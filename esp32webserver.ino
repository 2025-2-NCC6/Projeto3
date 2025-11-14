#include <WiFi.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "";
const char* password = "";

const int SOLDA = 21;

const int MOTOR_SOBE = 22;
const int MOTOR_DESCE = 23;

const int FERRAMENTA_1 = 4;
const int FERRAMENTA_2 = 5;
const int FERRAMENTA_3 = 36;
const int FERRAMENTA_4 = 37;

// Abrindo o servidor na porta 8000
AsyncWebServer server(80);

bool toolStateToggle = true;

void setup() {
  Serial.begin(115200);

  pinMode(SOLDA, OUTPUT);

  pinMode(MOTOR_SOBE, OUTPUT);
  pinMode(MOTOR_DESCE, OUTPUT);

  pinMode(FERRAMENTA_1, INPUT_PULLDOWN);
  pinMode(FERRAMENTA_2, INPUT_PULLDOWN);
  pinMode(FERRAMENTA_3, INPUT);
  pinMode(FERRAMENTA_4, INPUT);

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Conectado!");
  Serial.print("IP do ESP32: ");
  Serial.println(WiFi.localIP());

  // Rotas do servidor
  // Rota comando ascensor
  server.on("/ascensor", HTTP_GET, [](AsyncWebServerRequest *request) {
    if (request->hasParam("cmd")) {
      String cmd = request->getParam("cmd")->value();
      
      if (cmd == "levantar") {
        Serial.println("Comando: Levantar");
        digitalWrite(MOTOR_SOBE, HIGH);
        digitalWrite(MOTOR_DESCE, LOW);
        
      } else if (cmd == "descer") {
        Serial.println("Comando: Descer");
        digitalWrite(MOTOR_SOBE, LOW);
        digitalWrite(MOTOR_DESCE, HIGH);
        
      } else if (cmd == "parar") {
        Serial.println("Comando: Parar");
        digitalWrite(MOTOR_SOBE, LOW);
        digitalWrite(MOTOR_DESCE, LOW);
        
      } else {
        request->send(400, "text/plain", "Comando invalido");
        return;
      }
      
      // Resposta de sucesso para o Flask
      request->send(200, "text/plain", "Comando recebido e processado: " + cmd);
    } else {
      request->send(400, "text/plain", "Parametro 'cmd' faltando");
    }
  });

  // Rota ferramentas
  server.on("/status", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Leitura dos pinos de sensores
    bool status_ferramenta_1 = (digitalRead(FERRAMENTA_1) == HIGH);
    bool status_ferramenta_2 = (digitalRead(FERRAMENTA_2) == HIGH);
    bool status_ferramenta_3 = (digitalRead(FERRAMENTA_3) == HIGH);
    bool status_ferramenta_4 = (digitalRead(FERRAMENTA_4) == HIGH);
    
    toolStateToggle = !toolStateToggle;

    String jsonResponse = "{\"tool-1\": " + String(status_ferramenta_1 ? "true" : "false") + ",";
    jsonResponse += "\"tool-2\": " + String(status_ferramenta_2 ? "true" : "false") + ",";
    jsonResponse += "\"tool-3\": " + String(status_ferramenta_3 ? "true" : "false") + ",";
    jsonResponse += "\"tool-4\": " + String(status_ferramenta_4 ? "true" : "false") + "}";
    
    request->send(200, "application/json", jsonResponse);
  });

  // Rota solda
  server.on("/solda_toggle", HTTP_GET, [](AsyncWebServerRequest *request) {
    if (request->hasParam("state")) {
      String state = request->getParam("state")->value();
      
      if (state == "ON") {
        Serial.println("Bancada de Solda: LIGADA");
        digitalWrite(SOLDA, HIGH);
        
      } else if (state == "OFF") {
        Serial.println("Bancada de Solda: DESLIGADA");
        digitalWrite(SOLDA, LOW);
        
      } else {
        request->send(400, "text/plain", "Comando de estado invalido (use ON ou OFF)");
        return;
      }
      
      request->send(200, "text/plain", "Solda status set to " + state);
    } else {
      request->send(400, "text/plain", "Parametro 'state' faltando");
    }
  });

  // Rota redirecionamento
  server.onNotFound([](AsyncWebServerRequest *request){
    request->send(404, "text/plain", "Nao encontrado");
  });

  server.begin();
  Serial.println("Servidor HTTP Async iniciado.");
}

void loop() {
  delay(10);
}