
# starsze poodejscie ktore wspiera tylko asynchroniczne wysylanie maila
from flask_mail import Mail, Message

from flask import Flask


class MailSender:
    _mail = None
    _sender = None

    def __init__(self, app: Flask, sender: str) -> None:
        MailSender._mail = Mail(app)
        MailSender._sender = sender

    @classmethod
    def send(cls, email: str, subject: str, content: str) -> None:
        mail_content = f'''
                    <html>
                        <body>
                            <div style="font-family:Consolas;margin:auto 100px;padding:5px;text-size:16px;color:white;background-color:grey">
                                {content}
                            </div>
                        </body>
                    </html>
                '''
        # nasza aplikacja flaskowa zleca mailowi ktory napiszemy (maila
        # moge np pobierac ze zmeinncyh srodowiskowych). tetowy2.kmprograms@gmail.com
        # prosze zebyc wyslal maila ktorego przygotowuje do
        message = Message(
            # temat wiadomosci email.
            subject=subject,
            # kto wysyla.
            sender=cls._sender,
            recipients=[email],
            # tresc wiadomosci
            html=mail_content,
        )
        cls._mail.send(message)
