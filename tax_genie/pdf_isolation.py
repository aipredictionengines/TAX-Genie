"""Bounded local PDF parsing via isolated spawned worker (prototype only).

A subprocess reduces direct in-process exposure, but does NOT provide an OS
sandbox, antivirus, seccomp, filesystem/network confinement or production safety.
"""
from __future__ import annotations
import multiprocessing as mp
import io
from pypdf import PdfReader

def _parse_worker(data: bytes, output):
    try:
        pdf=PdfReader(io.BytesIO(data),strict=True)
        if pdf.is_encrypted or len(pdf.pages)==0 or len(pdf.pages)>20:
            output.put(("error","UNSUPPORTED_PDF"))
            return
        lines=[]
        for page in pdf.pages:
            lines.append(page.extract_text() or "")
            if sum(map(len,lines))>250_000:
                output.put(("error","TEXT_TOO_LARGE"))
                return
        output.put(("ok",{"text":"\n".join(lines),"pages":len(pdf.pages)}))
    except Exception:
        output.put(("error","UNREADABLE_PDF"))

def parse_pdf_bounded(data: bytes, *, timeout: float=3.0) -> dict:
    if not isinstance(data,bytes) or len(data)==0 or len(data)>5*1024*1024 or not data.startswith(b"%PDF-"):
        raise ValueError("PDF rejected")
    if not (0.1 <= timeout <= 30):
        raise ValueError("Invalid timeout")
    ctx=mp.get_context("spawn")
    queue=ctx.Queue(maxsize=1)
    proc=ctx.Process(target=_parse_worker,args=(data,queue))
    proc.start()
    try:
        proc.join(timeout)
        if proc.is_alive():
            proc.terminate()
            proc.join(1)
            if proc.is_alive():
                proc.kill()
                proc.join()
            raise ValueError("PDF_PARSE_TIMEOUT")
        if proc.exitcode != 0:
            raise ValueError("PDF_PARSE_FAILED")
        try:
            state,payload=queue.get(timeout=0.25)
        except Exception as exc:
            raise ValueError("PDF_PARSE_NO_RESULT") from exc
        if state!="ok":
            raise ValueError(payload)
        return payload
    finally:
        queue.close()
        queue.join_thread()
