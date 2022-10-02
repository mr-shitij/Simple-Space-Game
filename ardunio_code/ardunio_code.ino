#include <ESP8266WiFi.h>

int latchPin = D4;
int dataPin = D3;
int clockPin = D2;

byte switchVar1 = 72;

const char* ssid = "";
const char* password = "";

WiFiServer server(80);
WiFiClient client;

void setup() {
  Serial.begin(9600);

  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, INPUT);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.setAutoConnect(true);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  server.begin();
  Serial.println("Server started");

  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}

void loop() {

  client = server.available();
  client.setNoDelay(1);
  if (!client) {
    return;
  }

  while(client.connected()){
    digitalWrite(latchPin,1);
    delayMicroseconds(5);
    digitalWrite(latchPin,0);
    switchVar1 = shiftIn(dataPin, clockPin);
    Serial.println(switchVar1);
    Serial.println("-------------------");

    client.print(switchVar1);
    client.flush();
  }
}

byte shiftIn(int myDataPin, int myClockPin) {
  int i;
  int temp = 0;
  int pinState;
  byte myDataIn = 0;

  pinMode(myClockPin, OUTPUT);
  pinMode(myDataPin, INPUT);
  for (i=7; i>=0; i--)
  {
    digitalWrite(myClockPin, 0);
    delayMicroseconds(1);
    temp = digitalRead(myDataPin);
    if (temp) {
      pinState = 1;
      myDataIn = myDataIn | (1 << i);
    }
    else {
      pinState = 0;
    }
    digitalWrite(myClockPin, 1);
  }
  return myDataIn;
}