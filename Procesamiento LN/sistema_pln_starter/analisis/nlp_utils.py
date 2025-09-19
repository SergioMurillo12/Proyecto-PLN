import re
import string
from typing import Iterable, List

# Conjunto de puntuación extendido
_PUNCT_SET = set(string.punctuation) | {'¿', '¡', '…', '“', '”', '«', '»', '–', '—'}

# Stopwords en español (usamos nltk si está disponible)
try:
    from nltk.corpus import stopwords
    _STOPWORDS_ES = set(stopwords.words('spanish'))
except Exception:
    _STOPWORDS_ES = {
        'de','la','que','el','en','y','a','los','del','se','las','por','un','para','con','no','una','su','al','lo',
        'como','más','pero','sus','le','ya','o','este','sí','porque','esta','entre','cuando','muy','sin','sobre',
        'también','me','hasta','hay','donde','quien','desde','todo','nos','durante','todos','uno','les','ni','contra',
        'otros','ese','eso','ante','ellos','e','esto','mí','antes','algunos','qué','unos','yo','otro','otras','otra',
        'él','tanto','esa','estos','mucho','quienes','nada','muchos','cual','poco','ella','estar','estas','algunas',
        'algo','nosotros','mi','mis','tú','te','ti','tu','tus','ellas','nosotras','vosotros','vosotras','os','mío',
        'mía','míos','mías','tuyo','tuya','tuyos','tuyas','suyo','suya','suyos','suyas','nuestro','nuestra','nuestros',
        'nuestras','vuestro','vuestra','vuestros','vuestras','esos','esas','estoy','estás','está','estamos','estáis',
        'están','ser','soy','eres','es','somos','sois','son','he','has','ha','hemos','habéis','han','haber','hay',
        'fue','fui','fuimos','fueron','era','eran','era','eras','éramos','erais','tenemos','tengo','tienen','tiene'
    }

def clean_text_to_tokens(
    text: str,
    extra_stopwords: Iterable[str] | None = None
) -> List[str]:
    """
    - Convierte a minúsculas
    - Elimina puntuación
    - Tokeniza palabras con acentos/ñ
    - Elimina stopwords
    """
    if not text:
        return []

    text = text.lower()
    pattern_punct = '[' + re.escape(''.join(_PUNCT_SET)) + ']'
    text = re.sub(pattern_punct, ' ', text)
    tokens = re.findall(r"[a-záéíóúüñ]+", text, flags=re.IGNORECASE)

    stops = set(_STOPWORDS_ES)
    if extra_stopwords:
        stops |= set(w.lower() for w in extra_stopwords)
    clean_tokens = [t for t in tokens if t not in stops]

    return clean_tokens
