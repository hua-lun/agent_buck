int numClicks = 0;
int counter2 = 0;
int counter = 0;
int ledPinWhite = 7;
int ledPinYellow = 3;
int ledPinBlue = 12;
int buttonApin = 9;
int buttonBpin = 8;

void setup() 
{
  pinMode(ledPinWhite, OUTPUT);
  pinMode(ledPinYellow, OUTPUT);
  pinMode(ledPinBlue, OUTPUT);
  pinMode(buttonApin, INPUT_PULLUP);   
  pinMode(buttonBpin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() 
{   
  if (digitalRead(buttonApin) == LOW) {
    digitalWrite(ledPinWhite, HIGH);
    counter = 1;
    numClicks++;
    Serial.println(numClicks);
    delay(250);
  }
  if (counter == 1) {
    digitalWrite(ledPinWhite, LOW);
    Serial.println("white on");
    counter = 0;
  }
  if (digitalRead(buttonBpin) == LOW) {
    digitalWrite(ledPinYellow, HIGH);
    delay(250);
    counter2 = 1;
  }
  if (counter2 == 1) {
    digitalWrite(ledPinYellow, LOW);
    Serial.println("yellow on");
    counter2 = 0;
  }
  if (numClicks == 10) {
    digitalWrite(ledPinBlue, HIGH);
    Serial.println("blue on");
    delay(250);
    numClicks = 0;
    digitalWrite(ledPinBlue, LOW);
  }
  
}
