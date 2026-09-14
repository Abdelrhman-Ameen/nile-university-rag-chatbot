"""Application identity is configuration, not a university fact for the LLM to guess."""

import re

from nu_chat.language import tokens

IDENTITY = {
    "en": "I'm NU Chat, a chatbot built specifically for Nile University in Egypt. I help with university questions using its documents, and I can also answer general questions. I'm an independent student project, not the university's official support service.",
    "ar": "أنا NU Chat، شات بوت معمول مخصوص لجامعة النيل في مصر. بساعدك في أسئلة الجامعة بالرجوع لمستنداتها، وكمان أقدر أجاوب على أسئلة عامة. أنا مشروع طلابي مستقل، مش خدمة الدعم الرسمية للجامعة.",
    "mixed": "أنا NU Chat، شات بوت معمول مخصوص لجامعة النيل في مصر. بساعدك في أسئلة الجامعة من مستنداتها، وكمان في الأسئلة العامة. أنا مشروع طلابي مستقل، مش الدعم الرسمي للجامعة.",
    "franco": "Ana NU Chat, chatbot ma3mool makhsoos le Nile University fi Masr. Basa3dak fe as2elet el gam3a men documents bta3etha, w kaman fe as2ela 3amma. Ana mashroo3 tollabi mosta2el, mesh el support el rasmi lel gam3a.",
}
GENERAL_NOTE = {
    "en": "I'm built specifically for Nile University, Egypt. This general answer isn't verified against university sources.",
    "ar": "أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.",
    "mixed": "أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.",
    "franco": "Ana ma3mool makhsoos le Nile University fi Masr. Di egaba 3amma, mesh ma3looma met2akked menha men sources el gam3a.",
}


def identity_question(question: str) -> bool:
    text = " ".join(tokens(question))
    return bool(
        re.fullmatch(
            r"(?:(?:no|but|okay|لا|طيب|طب|يعني) )?(?:who are you|what are you|"
            r"introduce yourself|انت مين|مين انت|انتي مين|انت ايه|عرفني بنفسك|عرف نفسك|"
            r"enta meen|enta min|enta meeen|meen enta)",
            text,
        )
    )
