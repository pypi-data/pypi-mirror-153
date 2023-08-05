# The library can be used without PIL/Pillow
try:
    from PIL import Image
except ImportError:
    Image = None

from ._libimagequant import lib, ffi


def _pil_image_to_raw_bytes(image):
    """Get raw bytes from a PIL/Pillow image.

    :param PIL.Image.Image image: The image.

    :rtype: bytes
    :return: The image as raw bytes (``b"RGBARGBARGBA..."``).
    """
    return bytes([comp for pix in image.getdata() for comp in pix])


def _liq_palette_to_raw_palette(liq_palette):
    """Converts a liq_palette to a raw RGBA palette usable with PIL/Pillow image.

    :param liq_palette: The palette de convert.

    :rtype: list
    :return: The raw RGBA palette (``[r0, g0, b0, a0, r1, g1, b1, a1,...]``).
    """
    return sum(
        [[color.r, color.g, color.b, color.a] for color in liq_palette.entries], []
    )


def quantize_raw_rgba_bytes(
    image_data, width, height, dithering_level=1.0, max_colors=256
):
    """Converts an RGBA image to an optimized 8bit paletted image.

    :param bytes image_data: Raw RGBA image data (format: ``b"RGBARGBARGBA..."``).
    :param int width: Image's width.
    :param int height: Image's height.
    :param float dithering_level: The dithering level, from ``0.0`` (no
                                  dithering) to ``1.0`` (default: ``1.0``).
    :param int max_colors: Maximum number of color to use in the palette, from
                           ``1`` to ``256`` (default: ``256``).

    :rtype: (bytes, list)
    :return: The processed image bytes (each byte represents a pixel and its
             value is the index of a color from the palette), and the palette (
             format: ``[r0, g0, b0, a0, r1, g1, b1, a1,...]``).

    >>> import imagequant
    >>> imagequant.quantize_raw_rgba_bytes(
    ...     b"\\xFF\\x00\\x00\\xFF"
    ...     b"\\x00\\xFF\\x00\\xFF"
    ...     b"\\x00\\x00\\xFF\\xFF"
    ...     b"\\xFF\\xFF\\xFF\\xFF",
    ...     2, 2
    ... )
    (b'...', [...])
    """
    if len(image_data) != 4 * width * height:
        raise ValueError("image_data length do not match the given width and height")

    if not 0.0 <= dithering_level <= 1.0:
        raise ValueError("dithering_level must be a float between 0.0 and 1.0")

    if not 1 <= max_colors <= 256:
        raise ValueError("max_colors must be an integer between 1 and 256")

    liq_attr = lib.liq_attr_create()
    liq_attr.max_colors = max_colors

    liq_image = lib.liq_image_create_rgba(liq_attr, image_data, width, height, 0)

    liq_result_p = ffi.new("liq_result**")
    lib.liq_image_quantize(liq_image, liq_attr, liq_result_p)
    lib.liq_set_dithering_level(liq_result_p[0], dithering_level)

    raw_8bit_pixels = ffi.new("char[]", width * height)
    lib.liq_write_remapped_image(
        liq_result_p[0], liq_image, raw_8bit_pixels, width * height
    )

    pal = lib.liq_get_palette(liq_result_p[0])

    output_image_data = ffi.unpack(raw_8bit_pixels, width * height)
    output_palette = _liq_palette_to_raw_palette(pal)

    lib.liq_result_destroy(liq_result_p[0])
    lib.liq_image_destroy(liq_image)
    lib.liq_attr_destroy(liq_attr)
    ffi.release(raw_8bit_pixels)

    return output_image_data, output_palette


def quantize_pil_image(image, dithering_level=1.0, max_colors=256):
    """Converts an RGBA image to an optimized 8bit paletted image.

    :param PIL.Image.Image image: The image to process.
    :param float dithering_level: The dithering level, from ``0.0`` (no
                                  dithering) to ``1.0`` (default: ``1.0``).
    :param int max_colors: Maximum number of color to use in the palette, from
                           ``1`` to ``256`` (default: ``256``).

    :rtype: PIL.Image.Image
    :return: The processed image as a PIL/Pillow image.

    >>> import imagequant
    >>> input_image = Image.open("./example.png")
    >>> imagequant.quantize_pil_image(input_image)
    <PIL.Image.Image image mode=P size=... at ...>
    """
    if Image is None:
        raise ImportError("PIL or Pillow is required to use this function.")

    if image.mode != "RGBA":
        image = image.convert(mode="RGBA")

    input_image_data = _pil_image_to_raw_bytes(image)

    output_image_data, output_palette = quantize_raw_rgba_bytes(
        input_image_data,
        image.width,
        image.height,
        dithering_level=dithering_level,
        max_colors=max_colors,
    )

    output_image = Image.frombytes(
        "P",
        [image.width, image.height],
        output_image_data,
        decoder_name="raw",
    )
    output_image.putpalette(output_palette, rawmode="RGBA")

    return output_image
