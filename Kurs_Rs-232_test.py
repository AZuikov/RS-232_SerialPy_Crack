'''
Программа тестирует последовательный COM порт устройства и
подбирает его режимы работы, если они заранее не известны.
На порт посылается известный запрос и ожидается какой-либо
ответ от утсройства

'''

import time
import serial

def WriteStrToFile(InputStr, fileName):
    print('Запись в файл {0} ...'.format(fileName))
    f=open(fileName,'a')
    f.write('============================\n')
    f.write(str(InputStr) + '\n')
    f.write('============================\n')
    f.close()
    print('Успешно...')

def SendMessageRs232(SerialDevice, SendStr, PrintAnswer = False):
    try:
        SerialDevice.write(SendStr)
    except serial.serialutil.SerialTimeoutException:
        print('Нет ответа...')
        return None
    print('PC >>> {0} >>> {1}'.format(SerialDevice.name,SendStr))
    line = SerialDevice.readline()
    if PrintAnswer == True and line != b'':
        # Если получена не пустая строка, значит настройки могут быть
        # рассмотрены как рабочие
        print('PC <<< {0} <<< {1}'.format(SerialDevice.name, line))
        return line
    else:
        # Если получена пустая строка, значит настройки не рабочие
        print('Нет ответа...')
        return None


def CrackSerialPort():
    # команда которую будем отправлять на устройство
    #InputCommandStr = b'*idn?\r\n'
    #InputCommandStr = b'cps_int_ext\r'
    print ("Введиет номер  последовательного порта Windows (если порт COM1 - введите цифру 1): ")
    PortNumber = input()
    if PortNumber.isdigit() == False:
        print("Вы ввели некорректный номер порта...")
        return -2


    print("Введите команду, которую нужно отправить на порт прибора:")
    MyString = input()

    InputCommandStr = MyString.encode("utf-8")

    # создаем объект
    MyTestSerialDevice=serial.Serial()
    # в моей системе есть только один последовательный порт COM1
    MyTestSerialDevice.port = 'COM' + PortNumber
    MyTestSerialDevice.timeout = 1 # количество секунд (1 секунда для простого опроса прибора достаточное время)
    MyTestSerialDevice.write_timeout = 1 # пауза между отправками команды на прибор


    # создаем списки с возможными настройками порта
    # исходя из документации для pyserial
    # MyBuadLst = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
    #MyBuadLst = [ 2400, 4800, 9600, 19200, 38400, 57600, 115200]
    MyBuadLst = [9600]
    MyByteSizeLst = [serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS]
    MyParityLst = [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK, serial.PARITY_SPACE]
    MyStopBitLst = [serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO]
    MyXonnXoffLst = [True, False]
    MyDsrDtrLst = [True, False]
    MyRtsCtsLst  = [True, False]
    # комбинации конечных символов строки - взврат и перенос каретки
    MyEndSymbolLst = [b'', b'\n', b'\r', b'\n\r', b'\r\n']

    # последовательно вложенными циклами начинаем перебирать параметры работы порта
    print ('Начало работы...')
    Counter=0
    for x in MyBuadLst:
        MyTestSerialDevice.baudrate = x

        for y in MyByteSizeLst:
            MyTestSerialDevice.bytesize = y

            for z in MyParityLst:
                MyTestSerialDevice.parity = z

                for q in MyStopBitLst:
                    MyTestSerialDevice.stopbits  = q

                    for w in MyXonnXoffLst:
                        MyTestSerialDevice.xonxoff = w

                        for e in MyDsrDtrLst:
                            MyTestSerialDevice.dsrdtr = e

                            for r in MyRtsCtsLst:
                                MyTestSerialDevice.rtscts = r

                                for t in MyEndSymbolLst:
                                    ####
                                    try:
                                        MyTestSerialDevice.open()
                                    except serial.serialutil.SerialException:
                                        MyTestSerialDevice.close()
                                        continue
                                    # чистим буферы
                                    MyTestSerialDevice.reset_input_buffer()
                                    MyTestSerialDevice.reset_output_buffer()
                                    Result = SendMessageRs232(MyTestSerialDevice, InputCommandStr + t, True)
                                    if Result != None:
                                        #создаем строку с параметрами порта для записи в файл
                                        SerialPortSetting = '\n' + 'PortName: ' + str(MyTestSerialDevice.name) + '\n' + 'Baudrate: ' + str(MyTestSerialDevice.baudrate) + '\n' +\
                                            'Data bits: ' + str(MyTestSerialDevice.bytesize) + '\n' + 'Parity: ' + str(MyTestSerialDevice.parity) + '\n' +\
                                            'Stop bits: ' + str(MyTestSerialDevice.stopbits) + '\n' + 'Rts/Cts: ' + str(MyTestSerialDevice.rtscts) + '\n' +\
                                            'XonnXoff: ' + str(MyTestSerialDevice.xonxoff) + '\n' + 'Dsr/Dtr: ' + str(MyTestSerialDevice.dsrdtr) + '\n'
                                        try:
                                            WriteStrToFile("Команда: " + InputCommandStr.decode("utf-8")+' "' +str(t) +'" ' +"\n" +"Ответ: " + Result.decode("utf-8") + "\n" + SerialPortSetting, 'output.txt')
                                        except UnicodeDecodeError:
                                            print ("Ответ не поддается декодирования в читаемы вид, запись в файл не производится...")
                                    MyTestSerialDevice.close()
                                    Counter += 1
                                    print('Выполнено {0} итераций подбора...'.format(Counter))

    print ("Работа окончена...")


CrackSerialPort()