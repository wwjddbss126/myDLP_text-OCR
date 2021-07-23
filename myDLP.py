# -*- coding : utf-8 -*-
from enum import Flag
import re, datetime, os, smtplib, shutil, win32file, cv2, pytesseract, time
from numpy import record
import tkinter
from tkinter import *
from tkinter import messagebox as msg
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import *
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from pdf2image import convert_from_path

logName = 'myDLP_Log.txt'

def read_pdf(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return str(output_string.getvalue())

# 정규 표현식 참고: https://wikidocs.net/4308

def isRE(file_path):
    idnum_regexp = re.compile(r'\b(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}\b')
    return idnum_regexp.findall(file_path)

def isPDF(file_path):
    with open(file_path, 'rb') as f:
        sig = f.read(4)
    pdf_regexp = re.compile(r'^b\'%PDF\'$') # 0x25504446 == %PDF
    return pdf_regexp.match(str(sig))

def MsgBox(file_path, mode):
    if(mode=='Text-Based'):
        item = isRE(read_pdf(file_path))
    else:
        item = isRE(image_base(file_path))
    msg.showwarning('myDLP 탐지 알림', "개인(민감)정보  %d 건이 포함된 문서의 이동이 탐지되었습니다." %len(item))
 
def recordLog(type, mode, file_path):
    f = open(logName, 'a')
    f.write('Detection Date: %s\n'%str(datetime.datetime.now()))
    f.write('Detection type: %s\n'%type)    
    f.write('Detected Mode: %s\n'%mode)
    f.write('Matched File: %s\n'%file_path)
    if(mode=='Text-Based'):
        item = isRE(read_pdf(file_path))
    elif(mode=='Image-Based'):
        item = isRE(image_base(file_path))
    else:
        item = ''
    f.write('Matched Data: %s, Total %d item(s)\n\n'%(str(item), len(item)))
    f.close()

def openLog():
    os.startfile('.\%s\\'%logName)

def chooseFile(label_set):
    global file_path
    tmp = filedialog.askopenfilename(initialdir=".",title='Please select a PDF file')
    if(isPDF(tmp) != None):
        file_path = tmp
        label_set.configure(text='path: %s'%file_path)
        return file_path
    else:
        msg.showerror('File Type Error', "pdf 파일이 아닙니다.")
        return -1

def sendMail(to, subject, body):
    mail_sender = 'forjy4815@gmail.com'
    mail_pw = 'ubpricziaredhpya'
    mail_reciever = ttk.Entry.get(to)
    mail_subject = ttk.Entry.get(subject)
    mail_body = ttk.Entry.get(body)
    mail_filename = file_path
    
    mail_msg = MIMEMultipart()
    mail_msg['From'] = mail_sender
    mail_msg['To'] = mail_reciever
    mail_msg['Subject'] = mail_subject

    mail_msg.attach(MIMEText(mail_body,'plain'))
    attachment = open(mail_filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment", filename= os.path.basename(mail_filename))
    mail_msg.attach(part)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(mail_sender, mail_pw)
    s.sendmail(mail_sender, mail_reciever, mail_msg.as_string())
    s.quit()

    checkinfo('EMAIL', file_path)
    msg.showinfo("myDLP", "Successfully Sent Mail to %s!"%mail_reciever)

def checkinfo(type, file_path):
    if(len(isRE(read_pdf(file_path))) != 0):
        MsgBox(file_path, 'Text-Based')
        recordLog(type, 'Text-Based', file_path)
    elif(len(isRE(read_pdf(file_path))) == 0):
        if(len(isRE(image_base(file_path))) != 0):
            MsgBox(file_path, 'Image-Based')
            recordLog(type, 'Image-Based', file_path)
        else:
            recordLog(type, 'None', file_path)

def image_base(file_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    res = ''
    pdfs = file_path
    pages = convert_from_path(pdfs, 350,  poppler_path = r"C:\\poppler-0.68.0\\bin")
    text = []
    i = 0
    for page in pages:
        imgName = "Page" + str(i) + ".jpg"
        dirName = 'myDLP_pdf2jpg'

        if not os.path.exists(dirName):
            os.makedirs(dirName)
        folder = ".\%s\\"%dirName + str(imgName)
        page.save(folder, "JPEG")
        config = ('-l kor+eng --oem 3 --psm 4')

        img_gray = cv2.imread(folder, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.imread(folder, cv2.IMREAD_GRAYSCALE)

        text.append(pytesseract.image_to_string(img_gray, config=config))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        res += text[i]
        i = i+1

    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', str(res))
    # print(str(res).)
    # return str(res)

def moveUSB(file_path, usbPath):
        shutil.move(file_path, usbPath)
        checkinfo('MOVE TO USB', file_path)
        msg.showinfo("myDLP", "%s로 파일을 이동했습니다."%usbPath)

def copyUSB(file_path, usbPath):
    shutil.copy(file_path, usbPath)
    checkinfo('COPY TO USB', file_path)
    msg.showinfo("myDLP", "%s로 파일을 복사했습니다"%usbPath)

def getUSB():
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drname = '%c:\\' % chr(ord('A') + d)
            t = win32file.GetDriveType(drname)
            if t == win32file.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list

def gui(window):
    window.title("myDLP")
    window.geometry('580x240')
    window.iconbitmap('bob_bi_solid.ico')

    btn_set = Button(window, text = "Set Target PDF", command=lambda: chooseFile(label_set))
    btn_set.grid(row=0, column=0)

    btn_open = Button(window, text = "Open Log File", command=openLog)
    btn_open.grid(row=0, column=1)

    label_set = Label(window, text='Please select a PDF file')
    label_set.grid(row=1, column=0, columnspan=2)

    label_n1 = Label(window, text = "=======MAIL=======")
    label_n1.grid(row=3, column=0, columnspan=2)

    # MAIL
    label_to = Label(window, text = "To: ")
    label_to.grid(row=4, column=0)

    to = ttk.Entry(window, width = 15) # 수신 주소
    to.grid(row=4, column=1)

    label_subject = Label(window, text = "Subject: ")
    label_subject.grid(row=5, column=0)

    subject = ttk.Entry(window, width = 15) # 메일 제목
    subject.grid(row=5, column=1)
    
    label_body = Label(window, text = "Body: ")
    label_body.grid(row=6, column=0)

    body = ttk.Entry(window, width = 15) # 메일 본문
    body.grid(row=6, column=1)
    
    btn_mail = Button(window, text = "Send e-mail", command=lambda: sendMail(to, subject, body))
    btn_mail.grid(row=7, column=0, columnspan=2)

    # USB
    label_n2 = Label(window, text = "=======USB=======")
    label_n2.grid(row=8, column=0, columnspan=2)

    usbCombo = ttk.Combobox(window, values=getUSB(), width=15)
    usbCombo.current(0)
    usbCombo.grid(row=9, column=0, columnspan=2)
    usbPath = usbCombo.get()

    btn_move = Button(window, text = "Move to USB", command=lambda: moveUSB(file_path, usbPath))
    btn_move.grid(row=10, column=0)

    btn_copy = Button(window, text = "Copy to USB", command=lambda: copyUSB(file_path, usbPath))
    btn_copy.grid(row=10, column=1)

    label_n3 = Label(window, text = "======made by matiii======")
    label_n3.grid(row=11,column=0, columnspan=2)

def main():
    window = Tk()
    gui(window)
    window.mainloop()

if __name__ == "__main__":
    main()
