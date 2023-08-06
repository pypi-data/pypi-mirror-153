# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

import os
import functools
import concurrent.futures
from pypdfium2 import _pypdfium as pdfium
from pypdfium2._helpers import page_renderer
from pypdfium2._helpers.opener import PdfContext


def _process_page(index, render_meth, input_obj, password, **kws):
    with PdfContext(input_obj, password) as pdf:
        result = render_meth(pdf, index, **kws)
    return index, result


def render_pdf_base(
        render_meth,
        input_obj,
        page_indices = None,
        password = None,
        n_processes = os.cpu_count(),
        **kws
    ):
    """
    Rasterise multiple pages of a PDF using an arbitrary page rendering method.
    Base function for :func:`.render_pdf_tobytes` and :func:`.render_pdf_topil`.
    
    Parameters:
        input_obj (str | bytes | typing.BinaryIO):
            The PDF document to render. It may be given as file path, bytes, or byte buffer.
        page_indices (typing.Sequence[int]):
            A list of zero-based indices of the pages to render.
        password (typing.Optional[str | bytes]):
            A password to unlock the document, if encrypted.
        n_processes (int):
            The number of rendering processes to run in parallel (defaults to :func:`os.cpu_count`).
        kws (dict):
            Additional parameters to be passed to :func:`.render_page_base`.
    """
    
    with PdfContext(input_obj, password) as pdf:
        n_pages = pdfium.FPDF_GetPageCount(pdf)
    
    if page_indices is None or len(page_indices) == 0:
        page_indices = [i for i in range(n_pages)]
    if not all(0 <= i < n_pages for i in page_indices):
        raise ValueError("Out of range page index detected.")
    
    n_digits = len(str( max(page_indices)+1 ))
    invoke_renderer = functools.partial(_process_page, render_meth=render_meth, input_obj=input_obj, password=password, **kws)
    
    with concurrent.futures.ProcessPoolExecutor(n_processes) as pool:
        for index, image in pool.map(invoke_renderer, page_indices):
            suffix = str(index+1).zfill(n_digits)
            yield image, suffix


def render_pdf_tobytes(*args, **kws):
    """
    Render multiple pages of a PDF to bytes. See :func:`.render_pdf_base` and :func:`.render_page_tobytes`.
    
    Yields:
        :class:`tuple`, :class:`str`
    """
    yield from render_pdf_base(page_renderer.render_page_tobytes, *args, **kws)


def render_pdf_topil(*args, **kws):
    """
    Render multiple pages of a PDF to :mod:`PIL` images. See :func:`.render_pdf_base` and :func:`.render_page_topil`.
    
    Yields:
        :class:`PIL.Image.Image`, :class:`str`
    """
    yield from render_pdf_base(page_renderer.render_page_topil, *args, **kws)
