import smbus

from time import sleep

import RPi.GPIO as GPIO

import threading

import telepot

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

 

PWR_MGMT_1   = 0x6B

SMPLRT_DIV   = 0x19

CONFIG       = 0x1A

GYRO_CONFIG  = 0x1B

INT_ENABLE   = 0x38

ACCEL_XOUT_H = 0x3B

ACCEL_YOUT_H = 0x3D

ACCEL_ZOUT_H = 0x3F

GYRO_XOUT_H  = 0x43

GYRO_YOUT_H  = 0x45

GYRO_ZOUT_H  = 0x47

 

my_token = 'token'

bot = telepot.Bot(my_token)

updater = Updater(token = my_token)

 

msg = 'Your parents FELL DOWN!!!! '

telegram_id = 'id'

 

buzzer = 23

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)

pwm = GPIO.PWM(buzzer, 262)

pwm.start(0)

 

flag = False

 

def MPU_Init():

	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

	

	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

	

	bus.write_byte_data(Device_Address, CONFIG, 0)

	

	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

 

def read_raw_data(addr):

        high = bus.read_byte_data(Device_Address, addr)

        low = bus.read_byte_data(Device_Address, addr+1)

    

        value = ((high << 8) | low)

        

        if(value > 32768):

                value = value - 65536

        return value

 

bus = smbus.SMBus(1) 	

Device_Address = 0x68

 

# piezo

def buzzerOn():

    GPIO.output(buzzer, GPIO.HIGH)

    pwm.start(100.0)

    sleep(3)

    pwm.stop()

    

def buzzerOff():

    GPIO.output(buzzer, GPIO.LOW)

    pwm.stop()

    

# telegram location

def cmd_task_buttons(update, context):

    task_buttons = [

        [InlineKeyboardButton('Location', callback_data=1 )]

    ]

 

    reply_markup = InlineKeyboardMarkup(task_buttons)

 

    context.bot.send_message(

        chat_id=update.message.chat_id

        , text="Track your parents' location."

        , reply_markup=reply_markup

    )

    

def cb_button(update, context):

    query = update.callback_query

    data = query.data

 

    context.bot.send_chat_action(

        chat_id=update.effective_user.id

        , action=ChatAction.TYPING

    )

 

    context.bot.edit_message_text(

        text='I think your parents are indoor..'.format( data )

        , chat_id=query.message.chat_id

        , message_id=query.message.message_id

    )

 

def add_handler(cmd, func):

       updater.dispatcher.add_handler(CommandHandler(cmd, func))

 

add_handler('map', cmd_task_buttons)

 

def callbsck_handler(func):

        updater.dispatcher.add_handler(CallbackQueryHandler(func))

 

callbsck_handler(cb_button)

 

def location():

    updater.start_polling()

    updater.idle()

    

threads = []

threads1 = []

threads2 = []

 

def result1():

    local_threads = []

    t2 = threading.Thread(target=buzzerOn)

    local_threads.append(t2)

    

    for thread in local_threads:

        thread.start()

        

for thread in threads:

    thread.join()

    

def result2():

    local_thread = []

    t3 = threading.Thread(target=buzzerOff)

    local_thread.append(t3)

    

    for thread1 in local_thread:

        thread1.start()

        

for thread1 in threads1:

    thread1.join()

    

def result3():

    local_thread1 = []

    t1 = threading.Thread(target=location)

    local_thread1.append(t1)

    

    for thread2 in local_thread1:

        thread2.start()

    

for thread2 in threads2:

    thread2.join()


MPU_Init()


def MPU_data():
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0

    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0

try:

    while True:

        #result3() # error
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)

        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)

        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0

        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0
        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", " Gy=%.2f" %Gy, u'\u00b0'+ "/s", " Gz=%.2f" %Gz, u'\u00b0'+ "/s", " Ax=%.2f g" %Ax, " Ay=%.2f g" %Ay, " Az=%.2f g" %Az)

        

        # fall_left: Ax <= -0.1 and Ax > -0.25

        # fall_right: Ax >= 0.24 and Ax < 0.38

        

        if (Az > 0.7 and Az <= 0.9 and Gz < -0.75) or (Az <= -0.7 and Az > -0.9):

            print("Fall detected!!")

            sleep(3)
            #mpu
            for(int i=0; i<5;i++):
                acc_x = read_raw_data(ACCEL_XOUT_H)
                acc_y = read_raw_data(ACCEL_YOUT_H)
                acc_z = read_raw_data(ACCEL_ZOUT_H)

                gyro_x = read_raw_data(GYRO_XOUT_H)
                gyro_y = read_raw_data(GYRO_YOUT_H)
                gyro_z = read_raw_data(GYRO_ZOUT_H)

                Ax = acc_x/16384.0
                Ay = acc_y/16384.0
                Az = acc_z/16384.0

                Gx = gyro_x/131.0
                Gy = gyro_y/131.0
                Gz = gyro_z/131.0
                print ("2Gx=%.2f" %Gx, u'\u00b0'+ "/s", " 2Gy=%.2f" %Gy, u'\u00b0'+ "/s", " 2Gz=%.2f" %Gz, u'\u00b0'+ "/s", " Ax=%.2f g" %Ax, " Ay=%.2f g" %Ay, " Az=%.2f g" %Az)

                if(Az > 0.7 and Az <= 0.9) or Gz < -0.75 or (Az <= -0.7 and Az > -0.9):
                    result1()#on
                    print("onnnnn")
                    print(i)

                    sleep(7)
                   for(int j=0;j<5;i++):
                       acc_x = read_raw_data(ACCEL_XOUT_H)
                       acc_y = read_raw_data(ACCEL_YOUT_H)
                       acc_z = read_raw_data(ACCEL_ZOUT_H)

                       gyro_x = read_raw_data(GYRO_XOUT_H)
                       gyro_y = read_raw_data(GYRO_YOUT_H)
                       gyro_z = read_raw_data(GYRO_ZOUT_H)

                       Ax = acc_x/16384.0
                       Ay = acc_y/16384.0
                       Az = acc_z/16384.0

                       Gx = gyro_x/131.0
                       Gy = gyro_y/131.0
                       Gz = gyro_z/131.0
                       print ("3Gx=%.2f" %Gx, u'\u00b0'+ "/s", " 3Gy=%.2f" %Gy, u'\u00b0'+ "/s", " 3Gz=%.2f" %Gz, u'\u00b0'+ "/s", " Ax=%.2f g" %Ax, " Ay=%.2f g" %Ay, " Az=%.2f g" %Az)
                       
                       if(Az > 0.7 and Az <= 0.9) or Gz < -0.75 or (Az <= -0.7 and Az > -0.9):

                           print(j)
                           bot.sendMessage(chat_id = telegram_id, text=msg)
                           break

                        else:
                            print("off")
                            result2()#off

                    break

                else:
                    print(i)
                    continue


        else:

            result2()#off

	 	

        sleep(1)

 

except KeyboardInterrupt:

    print("\nInterrupted!")

except:

    print("\nClosing socket")

finally:

    bus.close()

 

GPIO.cleanup()
