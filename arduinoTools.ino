// Pinos dos LDRs
const int LDR1 = A0;
const int LDR2 = A1;

// Pinos do LED RGB 1
const int LED1_R = 8;
const int LED1_G = 9;

// Pinos do LED RGB 2
const int LED2_R = 7;
const int LED2_G = 6;

// Pinos ESP32
const int SIGNAL1 = 4;
const int SIGNAL2 = 3;

// Limites dos LDRs
const int LIMIAR1 = 500;
const int LIMIAR2 = 500;

void setup() {
  Serial.begin(9600);

  // Define os pinos como saída
  pinMode(LED1_R, OUTPUT);
  pinMode(LED1_G, OUTPUT);
  pinMode(LED2_R, OUTPUT);
  pinMode(LED2_G, OUTPUT);
}

void loop() {
  // Leitura dos sensores
  int valorLDR1 = analogRead(LDR1);
  int valorLDR2 = analogRead(LDR2);

  // Controle do LED 1
  if (valorLDR1 > LIMIAR1) {
    // Ferramenta no lugar
    digitalWrite(LED1_R, LOW);
    digitalWrite(LED1_G, HIGH);
    digitalWrite(SIGNAL1, HIGH);
  } else {
    // Ferramenta retirada
    digitalWrite(LED1_R, HIGH);
    digitalWrite(LED1_G, LOW);
    digitalWrite(SIGNAL1, LOW);
  }
  
  // Controle do LED 2
  if (valorLDR2 > LIMIAR2) {
    // Ferramenta no lugar
    digitalWrite(LED2_R, LOW);
    digitalWrite(LED2_G, HIGH);
    digitalWrite(SIGNAL2, HIGH);
  } else {
    // Ferramenta retirada
    digitalWrite(LED2_R, HIGH);
    digitalWrite(LED2_G, LOW);
    digitalWrite(SIGNAL2, LOW);
  }

  delay(200);
}