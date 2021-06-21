

#include <DHT.h>;

//Constants
#define DHTPIN 7  
#define DHTPIN2 7// what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
DHT dht2(DHTPIN2, DHTTYPE);

//Variables
int chk;
float hum,hum2;  //Stores humidity value
float temp,temp2; //Stores temperature value



void setup() {
  dht.begin();
  dht2.begin();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  float smoke = analogRead(A0);
  float smoke2 = analogRead(A1);
  hum = dht.readHumidity();
  temp= dht.readTemperature();
  hum2 = dht2.readHumidity();
  temp2= dht2.readTemperature();


  Serial.print(hum);
  Serial.print(temp);
  Serial.print(smoke);
  Serial.print(hum2);
  Serial.print(temp2);
  Serial.print(smoke2);
  delay(300);
}
