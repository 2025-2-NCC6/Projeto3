int inSolda = 2;
int inSobe = 3;
int inDesce = 4;

int outSolda = 5;
int outSobe = 6;
int outDesce = 7;

void setup() {

  pinMode(inSolda, INPUT);
  pinMode(inSobe, INPUT);
  pinMode(inDesce, INPUT);

  pinMode(outSolda, OUTPUT);
  pinMode(outSobe, OUTPUT);
  pinMode(outDesce, OUTPUT);
}

void loop() {
  if (digitalRead(inSolda) == 1) {
    digitalWrite(outSolda, HIGH);
  } else {
    digitalWrite(outSolda, LOW);
  }

  if (digitalRead(inSobe) == 1) {
    digitalWrite(outSobe, HIGH);
  } else {
    digitalWrite(outSobe, LOW);
  }

  if (digitalRead(inDesce) == 1) {
    digitalWrite(outDesce, HIGH);
  } else {
    digitalWrite(outDesce, LOW);
  }

}