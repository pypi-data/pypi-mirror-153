"""
Functions and classes for heif images to read and write.
"""

from copy import deepcopy
from typing import Any, Dict, Iterator, List, Union
from warnings import warn

from _pillow_heif_cffi import ffi, lib
from PIL import Image, ImageOps, ImageSequence

from ._libheif_ctx import LibHeifCtx, LibHeifCtxWrite
from ._options import options
from .constants import HeifChannel, HeifChroma, HeifColorspace, HeifFiletype
from .error import HeifError, HeifErrorCode, check_libheif_error
from .misc import _get_bytes, set_orientation
from .private import (
    create_image,
    heif_ctx_as_dict,
    read_color_profile,
    read_metadata,
    retrieve_exif,
    retrieve_xmp,
    set_color_profile,
    set_exif,
    set_metadata,
    set_xmp,
)


class HeifImageBase:
    """Base class for :py:class:`HeifImage` and :py:class:`HeifThumbnail`"""

    size: tuple
    """Width and height of the image."""

    def __init__(self, heif_ctx: Union[LibHeifCtx, dict], handle):
        self._img_data: Dict[str, Any] = {}
        self._heif_ctx = heif_ctx
        self._colorspace = HeifColorspace.RGB
        if isinstance(heif_ctx, LibHeifCtx):
            self._handle = ffi.gc(handle, lib.heif_image_handle_release)
            self.size = (
                lib.heif_image_handle_get_width(self._handle),
                lib.heif_image_handle_get_height(self._handle),
            )
        else:
            self._handle = None
            self.size = heif_ctx["size"]
            _img = create_image(self.size, self.chroma, self.bit_depth, heif_ctx["data"], stride=heif_ctx["stride"])
            self._img_to_img_data_dict(_img)

    @property
    def bit_depth(self):
        """Image channel pixel bit depth. Possible values: 8, 10, 12

        .. note:: When ``convert_hdr_to_8bit`` is True, return value will be always ``8``"""

        if isinstance(self._heif_ctx, dict):
            return self._heif_ctx["bit_depth"]
        return 8 if self._heif_ctx.to_8bit else lib.heif_image_handle_get_luma_bits_per_pixel(self._handle)

    @property
    def original_bit_depth(self):
        """Number of bits in colour channel, before it was decoded using ``convert_hdr_to_8bit`` parameter.

        .. note:: If ``convert_hdr_to_8bit`` is ``False`` then this field is always equal to ``bit_depth``

            This includes situations where image was created not from a file.

        :returns: An int value representing number of bits per color channel."""

        if self._handle is not None:
            return lib.heif_image_handle_get_luma_bits_per_pixel(self._handle)
        return self.bit_depth

    @property
    def has_alpha(self):
        """``True`` for images with ``alpha`` channel, ``False`` otherwise.

        :returns: "True" or "False" """

        if isinstance(self._heif_ctx, LibHeifCtx):
            return bool(lib.heif_image_handle_has_alpha_channel(self._handle))
        return self._heif_ctx["mode"] == "RGBA"

    @property
    def mode(self):
        """Returns “RGBA” for images with alpha channel, and “RGB” for images without.

        :returns: "RGB" or "RGBA" """

        return "RGBA" if self.has_alpha else "RGB"  # noqa

    @property
    def heif_img(self):
        self._load_if_not()
        return self._img_data.get("img", None)

    @property
    def data(self):
        """Decodes image and returns image data.

        :returns: ``bytes`` of the decoded image."""

        self._load_if_not()
        return self._img_data.get("data", None)

    @property
    def stride(self):
        """Decodes image and returns stride.

        :returns: ``int`` stride of the decoded image."""

        self._load_if_not()
        return self._img_data.get("stride", None)

    @property
    def chroma(self):
        """Chroma subsampling of the image.

        :returns: Value from :py:class:`~pillow_heif.HeifChroma`"""

        if self.bit_depth <= 8:
            return HeifChroma.INTERLEAVED_RGBA if self.has_alpha else HeifChroma.INTERLEAVED_RGB
        return HeifChroma.INTERLEAVED_RRGGBBAA_BE if self.has_alpha else HeifChroma.INTERLEAVED_RRGGBB_BE

    @property
    def color(self):
        """Colorspace used to decode the image.

        :returns: Value from :py:class:`~pillow_heif.HeifColorspace`"""

        return self._colorspace

    def to_pillow(self, ignore_thumbnails: bool = False) -> Image.Image:
        """Helper method to create :py:class:`PIL.Image.Image`

        :param ignore_thumbnails: Shall` info["thumbnails"] be empty or not.

        :returns: :py:class:`PIL.Image.Image` class created from this image."""

        image = Image.frombytes(
            self.mode,  # noqa
            self.size,
            self.data,
            "raw",
            self.mode,
            self.stride,
        )
        if isinstance(self, HeifImage):
            for k in ("exif", "xmp", "metadata"):
                image.info[k] = self.info[k]
            for k in ("icc_profile", "icc_profile_type", "nclx_profile"):
                if k in self.info:
                    image.info[k] = self.info[k]
            thumbnails = [] if ignore_thumbnails else deepcopy(self.thumbnails)
            image.info["thumbnails"] = thumbnails
            image.info["original_orientation"] = set_orientation(image.info)
        return image

    def load(self):
        """Decode image.

        Usually, you do not need to call this, image will be decoded automatically
        when accessing ``data`` or ``stride`` properties."""

        self._load_if_not()
        return self

    def unload(self):
        if self._handle is not None:
            self._img_data.clear()

    def _load_if_not(self):
        if self._img_data or self._handle is None:
            return
        p_options = lib.heif_decoding_options_alloc()
        p_options = ffi.gc(p_options, lib.heif_decoding_options_free)
        p_options.convert_hdr_to_8bit = int(self._heif_ctx.to_8bit)
        p_img = ffi.new("struct heif_image **")
        check_libheif_error(lib.heif_decode_image(self._handle, p_img, self.color, self.chroma, p_options))
        heif_img = ffi.gc(p_img[0], lib.heif_image_release)
        self._img_to_img_data_dict(heif_img)

    def _img_to_img_data_dict(self, heif_img):
        p_stride = ffi.new("int *")
        p_data = lib.heif_image_get_plane(heif_img, HeifChannel.INTERLEAVED, p_stride)
        stride = p_stride[0]
        data_length = self.size[1] * stride
        data_buffer = ffi.buffer(p_data, data_length)
        self._img_data.update(img=heif_img, data=data_buffer, stride=stride)


class HeifThumbnail(HeifImageBase):
    """Class represents a single thumbnail for a HeifImage."""

    def __init__(self, heif_ctx: Union[LibHeifCtx, dict], img_handle, thumb_id: int, img_index: int):
        if isinstance(heif_ctx, LibHeifCtx):
            p_handle = ffi.new("struct heif_image_handle **")
            check_libheif_error(lib.heif_image_handle_get_thumbnail(img_handle, thumb_id, p_handle))
            handle = p_handle[0]
        else:
            handle = None
        super().__init__(heif_ctx, handle)
        self.info = {
            "thumb_id": thumb_id,
            "img_index": img_index,
        }

    def __repr__(self):
        _bytes = f"{len(self.data)} bytes" if self._img_data else "no"
        return (
            f"<{self.__class__.__name__} {self.size[0]}x{self.size[1]} {self.mode} "
            f"with id = {self.info['thumb_id']} for img with index = {self.info['img_index']} "
            f"and with {_bytes} image data>"
        )

    def __deepcopy__(self, memo):
        heif_ctx = heif_ctx_as_dict(self.bit_depth, self.mode, self.size, self.data, stride=self.stride)
        return HeifThumbnail(heif_ctx, None, self.info["thumb_id"], self.info["img_index"])


class HeifImage(HeifImageBase):
    """Class represents one frame in a file."""

    def __init__(self, img_id: int, img_index: int, heif_ctx: Union[LibHeifCtx, dict]):
        additional_info = {}
        if isinstance(heif_ctx, LibHeifCtx):
            p_handle = ffi.new("struct heif_image_handle **")
            error = lib.heif_context_get_image_handle(heif_ctx.ctx, img_id, p_handle)
            if error.code != HeifErrorCode.OK and not img_index:
                error = lib.heif_context_get_primary_image_handle(heif_ctx.ctx, p_handle)
            check_libheif_error(error)
            handle = p_handle[0]
            _metadata = read_metadata(handle)
            _exif = retrieve_exif(_metadata)
            _xmp = retrieve_xmp(_metadata)
            additional_info["metadata"] = _metadata
            _color_profile = read_color_profile(handle)
            if _color_profile:
                if _color_profile["type"] in ("rICC", "prof"):
                    additional_info["icc_profile"] = _color_profile["data"]
                    additional_info["icc_profile_type"] = _color_profile["type"]
                else:
                    additional_info["nclx_profile"] = _color_profile["data"]
        else:
            handle = None
            _exif = None
            _xmp = None
            additional_info["metadata"] = []
            additional_info.update(heif_ctx.get("additional_info", {}))
        super().__init__(heif_ctx, handle)
        self.info = {
            "img_id": img_id,
            "exif": _exif,
            "xmp": _xmp,
        }
        self.info.update(**additional_info)
        self.thumbnails = self.__read_thumbnails(img_index)

    def __repr__(self):
        _bytes = f"{len(self.data)} bytes" if self._img_data else "no"
        return (
            f"<{self.__class__.__name__} {self.size[0]}x{self.size[1]} {self.mode} "
            f"with id = {self.info['img_id']}, {len(self.thumbnails)} thumbnails "
            f"and with {_bytes} image data>"
        )

    def load(self):
        super().load()
        for thumbnail in self.thumbnails:
            thumbnail.load()
        return self

    def unload(self):
        super().unload()
        for thumbnail in self.thumbnails:
            thumbnail.unload()
        return self

    def scale(self, width: int, height: int):
        """Rescale image by a specific width and height given in parameters.

        .. note:: Image will be scaled in place.

        :param width: new image width.
        :param height: new image height"""

        self._load_if_not()
        p_scaled_img = ffi.new("struct heif_image **")
        check_libheif_error(lib.heif_image_scale_image(self.heif_img, p_scaled_img, width, height, ffi.NULL))
        scaled_heif_img = ffi.gc(p_scaled_img[0], lib.heif_image_release)
        self.size = (
            lib.heif_image_get_primary_width(scaled_heif_img),
            lib.heif_image_get_primary_height(scaled_heif_img),
        )
        self._img_to_img_data_dict(scaled_heif_img)
        return self

    def add_thumbnails(self, boxes: Union[List[int], int]) -> None:
        """Add thumbnail(s) to an image.

        :param boxes: int or list of ints determining size of thumbnail(s) to generate for image.

        :returns: None."""

        if isinstance(boxes, list):
            boxes_list = boxes
        else:
            boxes_list = [boxes]
        self.load()
        for box in boxes_list:
            if box <= 3:
                continue
            if self.size[0] <= box and self.size[1] <= box:
                continue
            if self.size[0] > self.size[1]:
                thumb_height = int(self.size[1] * box / self.size[0])
                thumb_width = box
            else:
                thumb_width = int(self.size[0] * box / self.size[1])
                thumb_height = box
            thumb_height = thumb_height - 1 if (thumb_height & 1) else thumb_height
            thumb_width = thumb_width - 1 if (thumb_width & 1) else thumb_width
            if max((thumb_height, thumb_width)) in [max(i.size) for i in self.thumbnails]:
                continue
            p_new_thumbnail = ffi.new("struct heif_image **")
            error = lib.heif_image_scale_image(self.heif_img, p_new_thumbnail, thumb_width, thumb_height, ffi.NULL)
            check_libheif_error(error)
            new_thumbnail = ffi.gc(p_new_thumbnail[0], lib.heif_image_release)
            __size = (
                lib.heif_image_get_width(new_thumbnail, HeifChannel.INTERLEAVED),
                lib.heif_image_get_height(new_thumbnail, HeifChannel.INTERLEAVED),
            )
            p_dest_stride = ffi.new("int *")
            p_data = lib.heif_image_get_plane(new_thumbnail, HeifChannel.INTERLEAVED, p_dest_stride)
            dest_stride = p_dest_stride[0]
            data = ffi.buffer(p_data, __size[1] * dest_stride)
            __heif_ctx = heif_ctx_as_dict(self.bit_depth, self.mode, __size, data, stride=dest_stride)
            self.thumbnails.append(HeifThumbnail(__heif_ctx, None, 0, 0))

    def __read_thumbnails(self, img_index: int) -> List[HeifThumbnail]:
        result: List[HeifThumbnail] = []
        if self._handle is None or not options().thumbnails:
            return result
        thumbs_count = lib.heif_image_handle_get_number_of_thumbnails(self._handle)
        if thumbs_count == 0:
            return result
        thumbnails_ids = ffi.new("heif_item_id[]", thumbs_count)
        thumb_count = lib.heif_image_handle_get_list_of_thumbnail_IDs(self._handle, thumbnails_ids, thumbs_count)
        for i in range(thumb_count):
            result.append(HeifThumbnail(self._heif_ctx, self._handle, thumbnails_ids[i], img_index))
        return result


class HeifFile:
    """This class represents the :py:class:`~pillow_heif.HeifImage` classes container.

    To create :py:class:`~pillow_heif.HeifFile` object, use the appropriate factory functions.

    * :py:func:`~pillow_heif.open_heif`
    * :py:func:`~pillow_heif.from_pillow`

    .. note:: To get empty container to fill it later, create a class without parameters."""

    def __init__(self, heif_ctx: Union[LibHeifCtx, dict] = None, img_ids: list = None):
        if heif_ctx is None:
            heif_ctx = {}
        self._images: List[HeifImage] = []
        self.mimetype = heif_ctx.get_mimetype() if isinstance(heif_ctx, LibHeifCtx) else ""
        if img_ids:
            for i, img_id in enumerate(img_ids):
                self._images.append(HeifImage(img_id, i, heif_ctx))

    @property
    def original_bit_depth(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.original_bit_depth` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].original_bit_depth

    @property
    def bit_depth(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.bit_depth` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].bit_depth

    @property
    def size(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.size` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].size

    @property
    def mode(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.mode` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].mode

    @property
    def data(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.data` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].data

    @property
    def stride(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.stride` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].stride

    @property
    def chroma(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.chroma` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].chroma

    @property
    def color(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.color` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].color

    @property
    def has_alpha(self):
        """Points to :py:attr:`~pillow_heif.HeifImage.has_alpha` property of the
        first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].has_alpha

    @property
    def info(self):
        """Points to ``info`` dict of the first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].info

    @property
    def thumbnails(self):
        """Points to ``thumbnails`` of the first :py:class:`~pillow_heif.HeifImage`'s class in container.

        :exception IndexError: If there is no images."""

        return self._images[0].thumbnails

    def thumbnails_all(self, one_for_image: bool = False) -> Iterator[HeifThumbnail]:
        """Enums all thumbnails in all images.

        :param one_for_image: If set to ``True`` will return maximum one thumbnail for one image.

        :returns: Iterator for :py:class:`~pillow_heif.HeifThumbnail` classes."""

        for i in self:
            for thumb in i.thumbnails:
                yield thumb
                if one_for_image:
                    break

    def load(self, everything: bool = False):
        for img in self:
            img.load()
            if not everything:
                break
        return self

    def scale(self, width: int, height: int) -> None:
        """Scale first image in container. See :py:meth:`~pillow_heif.HeifImage.scale`"""

        self._images[0].scale(width, height)

    def add_from_pillow(self, pil_image: Image.Image, load_one=False):
        """Add image(s) to container.

        :param pil_image: ``PIL.Image`` class to get images from.
        :param load_one: should be only one frame loaded. Default=``False``"""

        for frame in ImageSequence.Iterator(pil_image):
            if frame.width > 0 and frame.height > 0:
                additional_info = {}
                for k in ("exif", "xmp", "metadata", "icc_profile", "icc_profile_type", "nclx_profile"):
                    if k in frame.info:
                        additional_info[k] = frame.info[k]
                if "xmp" not in additional_info and "XML:com.adobe.xmp" in frame.info:
                    additional_info["xmp"] = frame.info["XML:com.adobe.xmp"]
                if "xmp" in additional_info and isinstance(additional_info["xmp"], str):
                    additional_info["xmp"] = additional_info["xmp"].encode("utf-8")
                original_orientation = set_orientation(additional_info)
                if frame.mode == "P":
                    mode = "RGBA" if frame.info.get("transparency") else "RGB"
                    frame = frame.convert(mode=mode)
                elif frame.mode == "LA":
                    frame = frame.convert(mode="RGBA")
                elif frame.mode == "L":
                    frame = frame.convert(mode="RGB")

                if original_orientation is not None:
                    frame = ImageOps.exif_transpose(frame)
                # check image.bits / pallete.rawmode to detect > 8 bit or maybe something else?
                _bit_depth = 8
                self._add_frombytes(_bit_depth, frame.mode, frame.size, frame.tobytes(), add_info={**additional_info})
                for thumb in frame.info.get("thumbnails", []):
                    self._images[len(self._images) - 1].thumbnails.append(
                        self.__get_image_thumb_frombytes(
                            thumb.bit_depth,
                            thumb.mode,
                            thumb.size,
                            thumb.data,
                            stride=thumb.stride,
                        )
                    )
            if load_one:
                break
        return self

    def add_from_heif(self, heif_image):
        """Add image(s) to container.

        :param heif_image: ``HeifFile`` or ``HeifImage`` class to get images from."""

        if isinstance(heif_image, HeifFile):
            heif_images = list(heif_image)
        else:
            heif_images = [heif_image]
        for image in heif_images:
            image.load()
            additional_info = image.info.copy()
            additional_info.pop("img_id", None)
            self._add_frombytes(
                image.bit_depth,
                image.mode,
                image.size,
                image.data,
                stride=image.stride,
                add_info={**additional_info},
            )
            for thumb in image.thumbnails:
                self._images[len(self._images) - 1].thumbnails.append(
                    self.__get_image_thumb_frombytes(
                        thumb.bit_depth,
                        thumb.mode,
                        thumb.size,
                        thumb.data,
                        stride=thumb.stride,
                    )
                )
        return self

    def add_thumbnails(self, boxes: Union[List[int], int]) -> None:
        """
        Add thumbnail(s) to all images.

        :param boxes: int or list of ints determining size of thumbnail(s) to generate for images.

        :returns: None."""

        for img in self._images:
            img.add_thumbnails(boxes)

    def save(self, fp, **kwargs) -> None:
        """Saves image under the given fp.

        Keyword options can be used to provide additional instructions to the writer.
        If a writer does not recognise an option, it is silently ignored.

        Supported options:
            ``save_all`` - boolean. Should all images from ``HeiFile`` be saved.
            (default = ``True``)

            ``append_images`` - do the same as in Pillow.
            Accept ``HeifFile``, ``HeifImage`` and ``PIL.Image``

            ``quality`` - see :py:attr:`~pillow_heif._options.PyLibHeifOptions.quality`

            ``enc_params`` - tuple of name:value to pass to :ref:`x265 <hevc-encoder>` encoder.

        :param fp: A filename (string), pathlib.Path object or file object.

        :returns: None
        :raises: :py:exc:`~pillow_heif.HeifError` or :py:exc:`ValueError`"""

        save_all = kwargs.get("save_all", True)
        append_images = self.__heif_images_from(kwargs.get("append_images", [])) if save_all else []
        if not options().hevc_enc:
            raise HeifError(code=HeifErrorCode.ENCODING_ERROR, subcode=5000, message="No encoder found.")
        if not self._images and not append_images:
            raise ValueError("Cannot write empty image as HEIF.")
        heif_ctx_write = LibHeifCtxWrite()
        heif_ctx_write.set_encoder_parameters(kwargs.get("enc_params", []), kwargs.get("quality", options().quality))
        self._save(heif_ctx_write, not save_all, append_images)
        heif_ctx_write.write(fp)

    def __repr__(self):
        return f"<{self.__class__.__name__} with {len(self)} images: {[str(i) for i in self]}>"

    def __len__(self):
        return len(self._images)

    def __iter__(self):
        for _ in self._images:
            yield _

    def __getitem__(self, index):
        if index < 0 or index >= len(self._images):
            raise IndexError(f"invalid image index: {index}")
        return self._images[index]

    def __delitem__(self, key):
        if key < 0 or key >= len(self._images):
            raise IndexError(f"invalid image index: {key}")
        del self._images[key]

    def _save(self, ctx: LibHeifCtxWrite, save_one: bool, append_images: List[HeifImage]) -> None:
        enc_options = lib.heif_encoding_options_alloc()
        enc_options = ffi.gc(enc_options, lib.heif_encoding_options_free)
        for img in list(self) + append_images:
            img.load()
            new_img = create_image(img.size, img.chroma, img.bit_depth, img.data, stride=img.stride)
            set_color_profile(new_img, img.info)
            p_new_img_handle = ffi.new("struct heif_image_handle **")
            error = lib.heif_context_encode_image(ctx.ctx, new_img, ctx.encoder, enc_options, p_new_img_handle)
            check_libheif_error(error)
            new_img_handle = ffi.gc(p_new_img_handle[0], lib.heif_image_handle_release)
            set_exif(ctx, new_img_handle, img.info)
            set_xmp(ctx, new_img_handle, img.info)
            set_metadata(ctx, new_img_handle, img.info)
            for thumbnail in img.thumbnails:
                thumb_box = max(thumbnail.size)
                if max(img.size) > thumb_box > 3:
                    p_new_thumb_handle = ffi.new("struct heif_image_handle **")
                    error = lib.heif_context_encode_thumbnail(
                        ctx.ctx,
                        new_img,
                        new_img_handle,
                        ctx.encoder,
                        enc_options,
                        thumb_box,
                        p_new_thumb_handle,
                    )
                    check_libheif_error(error)
                    if p_new_thumb_handle[0] != ffi.NULL:
                        lib.heif_image_handle_release(p_new_thumb_handle[0])
            if save_one:
                break

    def _add_frombytes(self, bit_depth: int, mode: str, size: tuple, data, **kwargs):
        __ids = [i.info["img_id"] for i in self._images] + [i.info["thumb_id"] for i in self.thumbnails_all()] + [0]
        __new_id = 2 + max(__ids)
        __heif_ctx = heif_ctx_as_dict(bit_depth, mode, size, data, **kwargs)
        self._images.append(HeifImage(__new_id, len(self), __heif_ctx))
        return self

    def __get_image_thumb_frombytes(self, bit_depth: int, mode: str, size: tuple, data, **kwargs):
        __ids = [i.info["img_id"] for i in self._images] + [i.info["thumb_id"] for i in self.thumbnails_all()] + [0]
        __new_id = 2 + max(__ids)
        __heif_ctx = heif_ctx_as_dict(bit_depth, mode, size, data, **kwargs)
        __img_index = kwargs.get("img_index", len(self._images))
        return HeifThumbnail(__heif_ctx, None, __new_id, __img_index)

    @staticmethod
    def __heif_images_from(images: list) -> List[HeifImage]:
        """Accepts list of Union[HeifFile, HeifImage, Image.Image] and returns List[HeifImage]"""
        result = []
        for img in images:
            if isinstance(img, HeifImage):
                result.append(img)
            else:
                heif_file = from_pillow(img) if isinstance(img, Image.Image) else img
                result += list(heif_file)
        return result


def check_heif(fp):
    """Wrapper around `libheif.heif_check_filetype` function.

    .. note:: If `fp` contains less 12 bytes, then always return `HeifFiletype.NO`

    :param fp: See parameter ``fp`` in :func:`is_supported`

    :returns: Value from :py:class:`~pillow_heif.HeifFiletype` enumeration."""

    magic = _get_bytes(fp, 16)
    return HeifFiletype.NO if len(magic) < 12 else lib.heif_check_filetype(magic, len(magic))


def is_supported(fp) -> bool:
    """Checks if the given `fp` object contains a supported file type,
    by calling :py:func:`~pillow_heif.check_heif` function.

    Look at :py:attr:`~pillow_heif._options.PyLibHeifOptions.strict` property for additional info.

    :param fp: A filename (string), pathlib.Path object or a file object.
        The file object must implement ``file.read``,
        ``file.seek``, and ``file.tell`` methods,
        and be opened in binary mode.

    :returns: A boolean indicating if object can be opened."""

    magic = _get_bytes(fp, 16)
    heif_filetype = check_heif(magic)
    if heif_filetype == HeifFiletype.NO or (not options().avif and magic[8:12] in (b"avif", b"avis")):
        return False
    if heif_filetype in (HeifFiletype.YES_SUPPORTED, HeifFiletype.MAYBE):
        return True
    return not options().strict


def open_heif(fp, convert_hdr_to_8bit=True) -> HeifFile:
    """Opens the given HEIF image file.

    :param fp: See parameter ``fp`` in :func:`is_supported`
    :param convert_hdr_to_8bit: Boolean indicating should 10 bit or 12 bit images
        be converted to 8 bit images during loading.

    :returns: An :py:class:`~pillow_heif.HeifFile` object.
    :exception HeifError: If file is corrupted or is not in Heif format."""

    heif_ctx = LibHeifCtx(fp, convert_hdr_to_8bit)
    main_image_id = heif_ctx.get_main_img_id()
    top_img_ids = heif_ctx.get_top_images_ids()
    top_img_list = [main_image_id] + [i for i in top_img_ids if i != main_image_id]
    return HeifFile(heif_ctx, top_img_list)


def read_heif(fp, convert_hdr_to_8bit=True) -> HeifFile:
    """Opens the given HEIF image file and decodes all images.

    .. note:: In most cases it better to call :py:meth:`~pillow_heif.open_heif`, and
        let images decoded automatically only when needed.

    :param fp: See parameter ``fp`` in :func:`is_supported`
    :param convert_hdr_to_8bit: Boolean indicating should 10 bit or 12 bit images
        be converted to 8 bit images during loading.

    :returns: An :py:class:`~pillow_heif.HeifFile` object.
    :exception HeifError: If file is corrupted or is not in Heif format."""

    heif_file = open_heif(fp, convert_hdr_to_8bit)
    heif_file.load(everything=True)
    return heif_file


def from_pillow(pil_image: Image.Image, load_one: bool = False) -> HeifFile:
    """Creates :py:class:`~pillow_heif.HeifFile` from a Pillow Image.

    :param pil_image: Pillow :external:py:class:`~PIL.Image.Image` class
    :param load_one: If ``True``, then all frames will be loaded.

    :returns: An :py:class:`~pillow_heif.HeifFile` object."""

    return HeifFile().add_from_pillow(pil_image, load_one)


# --------------------------------------------------------------------
# DEPRECATED FUNCTIONS.
# pylint: disable=unused-argument
# pylint: disable=redefined-builtin


def check(fp):
    warn("Function `check` is deprecated, use `check_heif` instead.", DeprecationWarning)
    return check_heif(fp)  # pragma: no cover


def open(fp, *, apply_transformations=True, convert_hdr_to_8bit=True):  # noqa
    warn("Function `open` is deprecated and will be removed, use `open_heif` instead.", DeprecationWarning)
    return open_heif(fp, convert_hdr_to_8bit=convert_hdr_to_8bit)  # pragma: no cover


def read(fp, *, apply_transformations=True, convert_hdr_to_8bit=True):  # noqa
    warn("Function `read` is deprecated and will be removed, use `open_heif` instead.", DeprecationWarning)
    return open_heif(fp, convert_hdr_to_8bit=convert_hdr_to_8bit)  # pragma: no cover
