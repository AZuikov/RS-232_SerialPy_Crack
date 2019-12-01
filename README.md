# RS-232_SerialPy_Crack
В моей практике возникали ситуации, когда необходимо было работать с устройствами через последовательный порт. Но информация о настройках порта отсутствовала и получить эту информацию было невозможно...
Поэтому я написал этот скрипт. Все очень просто.

Программа перебирает все возможные сочетания настроек порта, и наиболее удачные конфигурации записываются в текстовый файл. После ыполнения программы можно выбрать наиболее удачный вариант настроек.
От пользователя только нужно ввести номер последовательного порта и какую-нибудь тестовую команду, на которую устройство должно как-то ответить (например запрос модели или серийного номера).

Важно отметить, что программа корректно работает, только с контроллерами "PCI" или их более поздними версиями.
Контроллеры, которые подключаются через юсб корректно не работали.

Среднее время подбора для одной из скоростей, примерно 45 минут. Поэтому если есть каке-то ориентиры по настройками, лишние параетры можно отключить в коде.

Ссылка на видео: https://youtu.be/gtO0oKKvPfI

==============================================================================================

In my practice, there were situations when it was necessary to work with devices through a serial port. But there was no information about the port settings and it was impossible to get this information ...
So I wrote this script. Everything is very simple.

The program enumerates all possible combinations of port settings, and the most successful configurations are written to a text file. After completing the program, you can select the most successful option settings.
From the user, you only need to enter the serial port number and some test command to which the device must somehow respond (for example, requesting a model or serial number).

It is important to note that the program works correctly, only with "PCI" controllers or their later versions.
Controllers that connect via USB did not work correctly.

The average fitting time for one of the speeds is approximately 45 minutes. Therefore, if there are any guidelines for the settings, extra parameters can be disabled in the code.

Link to video: https://youtu.be/gtO0oKKvPfI
