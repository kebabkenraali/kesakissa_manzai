# Kesäkissa

AI-äänin toteutettu animoitu lyhytelokuva äidin ja pojan kahvipöytäkeskustelusta.

**Katso elokuva:** https://kebabkenraali.github.io/kesakissa_manzai/

## Mitä tässä on

- Yksi itsenäinen HTML-tiedosto (`index.html`), joka sisältää koko animaation, kameratyön ja tekstitykset.
- 43 suomenkielistä AI-ääniraitaa (`audio/`) — Microsoft Edge TTS: `fi-FI-NooraNeural` (äiti) ja `fi-FI-HarriNeural` (poika).
- Kuvakohtaiset taustat (parveke äidille, eteinen ja ulko-ovi pojalle), etu- ja sivuprofiilit, eleet sekä hidastetut kameran liikkeet.
- Vuorojen kestot on sovitettu ääniraitojen mukaan: jokaisella vuorolla on 0,55 s marginaali ennen seuraavaa kuvaa.

## Käyttö

Avaa `index.html` selaimessa tai käytä yllä olevaa GitHub Pages -osoitetta. Äänet toimivat paikallisestikin, koska ne ovat samassa hakemistossa suhteellisilla poluilla.

Näppäimet: `välilyönti` = tauko, `←` / `→` = siirry 5 s, ja edistymispalkista voi hyppiä kohtaukseen. Hakkeella `#t=0` voi avata tietyn kohdan suoraan.

## Äänien uudelleengenerointi

```bash
pip install edge-tts
python generoi_aani.py
```

Skripti lukee vuorot `index.html`:stä ja kirjoittaa MP3-tiedostot `audio/`-hakemistoon.

---

Tyyli: yksinkertaiset geometriset hahmot ja paksut ääriviivat. Käsikirjoitus perustuu perheen suusta kuultuun dialogiin.
