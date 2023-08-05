"""
pyOpenRPA open license
pyOpenRPA открытая лицензия

Copyright (c) 2019 Ivan Maslov
Правообладатель: 2019 Маслов Иван Дмитриевич

Текст лицензии см. в файле: LICENSE.PDF (в корне репозитория) или по адресу: https://pyopenrpa.ru/license/oferta.pdf

https://stackoverflow.com/questions/40574732/windows-data-storage-for-all-users

certificate.key

"""
import os
import sys
import time
gProgramDataPathStr = "C:\\ProgramData"
gProgramDataPORPathStr = os.path.join(gProgramDataPathStr, "pyOpenRPA")
gProgramDataCertificateFilePathStr = os.path.join(gProgramDataPORPathStr, "certificate.key")

# TODO Изменить права, чтобы другие пользователи могли править

if not os.path.exists(gProgramDataPORPathStr): os.mkdir(gProgramDataPORPathStr)

def CertificateExists() -> bool:
    """Check if the certificate key has been inserted

    :return: True - certificate key has been inserted; False - not has been inserted
    :rtype: bool
    """
    return os.path.exists(gProgramDataCertificateFilePathStr)

def CertificateKeySet(inCertificateKeyStr: str):
    """Get the certificate key string

    :param inCertificateKeyStr: Certificate key string (see license.pdf)
    :type inCertificateKeyStr: str
    """
    lFile = open(gProgramDataCertificateFilePathStr, "w", encoding="utf8")
    lFile.write(inCertificateKeyStr)
    lFile.close()

def CertificateKeyGet() -> str or None:
    """Get the certificate key from file

    :return: Certificate key (see license.pdf)
    :rtype: str or None (if key is not set)
    """
    
    lCertificateKeyStr=None
    if CertificateExists():
        lFile = open(gProgramDataCertificateFilePathStr, "r", encoding="utf8")
        lCertificateKeyStr = lFile.read()
        lFile.close()
    return lCertificateKeyStr

def ConsoleVerify() -> bool:
    """ Write info about certificate which has been detected on the machine

    :return: true - certificate exists
    :rtype: bool
    """
    lCertificateExistsBool = False
    if "PYOPENRPA_NODISP" not in os.environ:
        lCertificateExistsBool = True


        lCertificateKeyStr = CertificateKeyGet()
        if lCertificateKeyStr is None:
            lTextStr = """
Цифровой сертификат pyOpenRPA не обнаружен. 

Получить или проверить сертификат, а также ознакомиться с текстом лицензионного соглашения Вы можете по адресу: 
https://pyopenrpa.ru/verification
Операция формирования сертификата является автоматизированной и занимает несколько секунд.

pyOpenRPA не использует какие-либо инструменты физической блокировки функциональности своего ПО.
По всем вопросам Вы можете обратиться к правообладателю, контакты см. по адресу: 
https://pyopenrpa.ru/Index/pyOpenRPA_product_service.pdf
Используя ПО pyOpenRPA Вы осознаете свою ответственность в случаях нарушения лицензионного законодательства и совершения неправомерных действий.

ВНИМАНИЕ! НЕЗНАНИЕ ЗАКОНА НЕ ОСВОБОЖДАЕТ ОТ ОТВЕТСТВЕННОСТИ.
        """
            
            print(lTextStr)
            os.environ["PYOPENRPA_NODISP"]="1"
            lCertificateExistsBool = False
            time.sleep(5)
            ConsoleAccept()
        else:
            lTextStr = """
Обнаружен цифровой сертификат pyOpenRPA: {0}. 

Проверить сертификат, а также ознакомиться с текстом лицензионного соглашения Вы можете по адресу: 
https://pyopenrpa.ru/verification

pyOpenRPA не использует какие-либо инструменты физической блокировки функциональности своего ПО.
По всем вопросам Вы можете обратиться к правообладателю, контакты см. по адресу: 
https://pyopenrpa.ru/Index/pyOpenRPA_product_service.pdf
Используя ПО pyOpenRPA Вы осознаете свою ответственность в случаях нарушения лицензионного законодательства и совершения неправомерных действий.

ВНИМАНИЕ! НЕЗНАНИЕ ЗАКОНА НЕ ОСВОБОЖДАЕТ ОТ ОТВЕТСТВЕННОСТИ.
            """.format(lCertificateKeyStr)
            print(lTextStr)
            os.environ["PYOPENRPA_NODISP"]="1"
    return lCertificateExistsBool

def ConsoleAccept():
    """ Start pyOpenRPA activation master

    :return: _description_
    :rtype: str
    """
    if "PYOPENRPA_NODISP" not in os.environ:
        lText="""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░    ░░░░░   ░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░    ░░░░░   ░░░░░░░░░░░░
░░░░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░░░░
░░░░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░░░░
░░░░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░   ░░░
░░░░░░░░░░░   ░░░░░    ░░░░░   ░░░    ░░░░░
░░░░░░░░░░░   ░░░░░    ░░░░░       ░░░░░░░░
░░░   ░░░░░   ░░░░░    ░░░░░    ░░░░░░░░░░░
░░░░░    ░░   ░░░░░    ░░    ░░░░░░░░░░░░░░
░░░░░░░       ░░░░░        ░░░░░░░░░░░░░░░░
░░░░░░░░░░    ░░░░░    ░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░    ░░░    ░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░         ░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░      ░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░                        ░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        """
        print(lText)
        time.sleep(2)
        lText="""
(RUS LANGUAGE) 
***********************************************
Добро пожаловать в систему активации pyOpenRPA!
***********************************************

pyOpenRPA - это открытое программное обеспечение класса RPA, которое разработано и зарегистрировано на территории Российской Федерации (Автор Иван Маслов, 2019г.). Все исходные коды доступны неограниченному кругу лиц для просмотра.
Данное ПО позволяет решить любые задачи, относящиеся к классу программной роботизации RPA.

Перед использованием просим убедиться в том, что Вы обладаете действующим цифровым сертификатом pyOpenRPA (далее сертификат).
Данный сертификат является свидетельством того, что Вы наделены правами в отношении pyOpenRPA в соответствии с законодательством Российской Федерации.

Получить или проверить сертификат, а также ознакомиться с текстом лицензионного соглашения Вы можете по адресу: 
https://pyopenrpa.ru/verification
Операция формирования сертификата является автоматизированной и занимает несколько секунд.

pyOpenRPA не использует какие-либо инструменты физической блокировки функциональности своего ПО.
По всем вопросам Вы можете обратиться к правообладателю, контакты см. по адресу: 
https://pyopenrpa.ru/Index/pyOpenRPA_product_service.pdf
Используя ПО pyOpenRPA Вы осознаете свою ответственность в случаях нарушения лицензионного законодательства и совершения неправомерных действий.

ВНИМАНИЕ! НЕЗНАНИЕ ЗАКОНА НЕ ОСВОБОЖДАЕТ ОТ ОТВЕТСТВЕННОСТИ.
        """
        #print(os.get_terminal_size())
        print(lText)
        os.environ["PYOPENRPA_NODISP"]="1"
        lCertificateKeyStr = input("Укажите код сертификата:")
        CertificateKeySet(inCertificateKeyStr=lCertificateKeyStr)