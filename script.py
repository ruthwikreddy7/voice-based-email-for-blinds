import smtplib
import speech_recognition as sr
import pyttsx3
import easyimap as e
import pywhatkit as kt
from email.message import EmailMessage

Sender_Email = 'lakkireddyruthwikreddy@gmail.com'

# Recognizer() is used for recognizing speech from an audio source
listener = sr.Recognizer()

# pyttsx3 is used for text-to-speech conversion
engine = pyttsx3.init()


def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def get_info():
    with sr.Microphone() as source:
        print('Listening...')
        listener.adjust_for_ambient_noise(source, duration=1)
        voice = listener.listen(source)
        try:
            info = listener.recognize_google(voice, show_all=True)
            transcript = info['alternative'][0]['transcript'].lower() if info else None
            if transcript:
                print(f'Recognized: {transcript}')
                return transcript
            else:
                talk('Sorry sir, could not understand your voice. Can you please repeat?')
                return get_info()
        except sr.UnknownValueError:
            talk('Sorry sir, could not understand your voice. Can you please repeat?')
            return get_info()
        except sr.WaitTimeoutError:
            talk('Listening timed out. Can you please repeat your choice?')
            return get_info()
        except sr.RequestError:
            talk('There was an error with the voice recognition service. Please try again later.')
            exit()



def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(Sender_Email, 'vwwy qrzq veft wlnv')  # Replace 'your_password' with the actual password

    email = EmailMessage()
    email['From'] = Sender_Email
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)

    server.send_message(email)
    server.quit()


def read_email():
    server = e.connect('imap.gmail.com', Sender_Email,
                       'vwwy qrzq veft wlnv')  # Replace 'your_password' with the actual password
    server.listids()

    talk('Please say the serial number of email that you want to read, starting from the latest')
    number = get_info()

    if number == "one":
        number = "1"
    elif number == "two":
        number = "2"
    elif number == "three":
        number = "3"
    elif number == "four":
        number = "4"
    elif number == "five":
        number = "5"
    elif number == "six":
        number = "6"
    elif number == "seven":
        number = "7"
    elif number == "eight":
        number = "8"
    else:
        number = "9"

    id = int(number) - 1
    email = server.mail(server.listids()[id])

    talk('email is from...')
    talk(email.from_addr)
    talk('subject of the email is...')
    talk(email.title)
    talk('body of the email is...')
    talk(email.body)

    server.quit()


# List of names that can be used to send mail
email_list = {
    'saket': 'sakethpaida@gmail.com',
    'satvik': 'sathwikreddylakkireddy@gmail.com',
    'rutvik': 'lruthwikreddy_csb203232@mgit.ac.in',
    'akshay': 'psaketh_csb203247@mgit.ac.in',
    'saiteja': 'tsaiteja_csb203254@mgit.ac.in'
}


def email_info():
    talk('Hi sir, I am your Assistant for today. To whom you want to send an email?')
    name = get_info()

    if name in email_list:
        receiver = email_list[name]
        print('Name: ' + name)
        print('Receiver: ' + receiver)

        talk('What is the subject of your email?')
        subject = get_info()
        talk('Tell me the text in your email')
        message = get_info()

        send_email(receiver, subject, message)
        talk('Thank you sir. Your email has been sent.')
    else:
        talk('Sorry sir. The name is not in the list. Exiting.')


# List of contacts that can be used to send messages
contacts = {
    'naresh': '+918179377675',
    'monu': '+919052022082',
    'aadi': '+919652568183',
    'siddharth': '+918019061109'


}


def chat():
    talk('Hi sir, I am your assistant for today. To whom you want to send a message?')
    name = get_info()

    if name in contacts:
        receiver = contacts[name]
        print('Name: ' + name)
        print('Number: ' + receiver)

        talk('Tell me the text that you want to send')
        message = get_info()
        print('Message: ' + message)

        print(f"Sending message to {receiver}: {message}")

        # Automatically send the message without waiting for user confirmation
        kt.sendwhatmsg_instantly(receiver, message)
        talk('Thank you sir for using me. Your message has been sent.')

        # Ask if the user wants to send more messages
        talk('Do you want to send more messages?')
        send_more = get_info()
        if 'yes' in send_more:
            chat()
        else:
            talk('Thank you sir. Have a nice day. Bye')
    else:
        talk('Sorry sir. The name is not in the list. Exiting.')


def start():
    talk('Do you want to use WhatsApp or email?')
    reply = get_info()
    print(reply)
    if reply == 'whatsapp':
        chat()
    elif reply == 'email':
        talk('Say SEND to send email, Say READ to read email, Say EXIT to exit')
        reply1 = get_info()
        if reply1 == 'send':
            email_info()
        elif reply1 == 'read':
            read_email()
        elif reply1 == 'exit':
            exit()
        else:
            talk('Invalid choice. Exiting.')


if __name__ == "__main__":
    start()
