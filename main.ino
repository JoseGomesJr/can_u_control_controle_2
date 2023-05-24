int motor_l = 6;
int motor_r = 5;
int val_r = 90;   
int val_l = 90;
int led_warning = DD7;
float ganho_p = 1.2;
bool saiu_esqueda = false;
bool saiu_direita = false;

int sensor_right = A3;
int sensor_left = A2;

//display A4 -> SDA A5 -> SCL
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setupDisplay(void) {
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
}

void setup() {
  Serial.begin(9600);

  pinMode(motor_l, OUTPUT);  // configura pino como saída
  pinMode(motor_r, OUTPUT);  // configura pino como saída
  pinMode(led_warning, OUTPUT);  // configura pino como saída
  pinMode(sensor_left, INPUT);
  pinMode(sensor_right, INPUT);

  digitalWrite(led_warning, LOW);
  analogWrite(motor_l, 0);
  analogWrite(motor_r, 0);

  setupDisplay();
  delay(5000);
}

void control_p(bool direction) {
  if(direction){
    val_r = val_r * ganho_p;
    Serial.println("Curva para direita");
    saiu_esqueda = true;
    val_l = 80;
  } else {
    Serial.println("Curva para esquerda");
    val_l = val_l * ganho_p;
    saiu_direita = true;
    val_r = 80;
  }
  
  digitalWrite(led_warning, HIGH);
  val_l = constrain(val_l,0,110);
  val_r = constrain(val_r,0,110);
}

void sensor_read(int sensor_right, int sensor_left) {
  if (sensor_right < 425) {
    control_p(true);
    return;
  }
  
  if(sensor_left < 330) {
    control_p(false);
    return;
  }

  digitalWrite(led_warning, LOW);
  saiu_esqueda = false;
  saiu_direita = false;
  val_l = 90;
  val_r = 90;
}

void printInformation(int leitura_l, int leitura_r) {
  float voltage_l = leitura_l * (5.0 / 1023.0);
  float voltage_r = leitura_r * (5.0 / 1023.0);

  display.clearDisplay();
  display.setCursor(0,0);
  display.println("L -> PWM: " + String(leitura_l) + "   " + String(voltage_l) + "V");
  display.println("R -> PWM: " + String(leitura_r) + "   " + String(voltage_r) + "V");
  display.display();
}

void loop() {
  int leitura_r = analogRead(sensor_right);
  int leitura_l = analogRead(sensor_left);
  
  Serial.print("Leitura da direita: ");
  Serial.println(leitura_r);
  Serial.print("Leitura da esquerda: ");
  Serial.println(leitura_l);
  
  analogWrite(motor_l, val_l);
  analogWrite(motor_r, val_r);

  sensor_read(leitura_r, leitura_l);

  printInformation(leitura_l, leitura_r);

  Serial.print("Potencia da esquerda: ");
  Serial.println(val_l);
  Serial.print("Potencia da direita: ");
  Serial.println(val_r);
}
