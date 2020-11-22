import pytest

from rabbitark.extractor import load


@pytest.mark.asyncio
@pytest.mark.parametrize("option", ["hitomi"])
async def test_download_hitomi(rabbitark):
    load()
    await rabbitark.start("1")


@pytest.mark.asyncio
@pytest.mark.parametrize("option", ["pixiv"])
async def test_download_pixiv(rabbitark):
    load()
    await rabbitark.start("9666585")


@pytest.mark.asyncio
@pytest.mark.parametrize("option", ["youtube"])
async def test_download_youtube(rabbitark):
    load()
    await rabbitark.start("PLB6rrfCPynfApD_C0yItgW5WLC0f-wDvG")
