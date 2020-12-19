#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include<WiFiUdp.h>

#define udpPort 4210

const char *ssid = "test";
const char *password = "password";

char packet[361];
int num = 0;

WiFiUDP UDP;
ESP8266WebServer server(80);

void handleRoot() {

  server.send(200, "text/html", "<h1>You are connected</h1>");

}

void setup() {

  delay(1000);
  
  Serial.begin(115200);
  Serial.println();
  Serial.print("Configuring access point…");
  
  WiFi.softAP(ssid, password);
  
  IPAddress myIP = WiFi.softAPIP();
  
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  
  server.on("/", handleRoot);
  server.begin();
  
  Serial.println("HTTP server started");

  UDP.begin(udpPort);
  Serial.print("Listening on UDP port ");
  Serial.println(udpPort);

}

void loop() {

  server.handleClient();

  int packetSize = UDP.parsePacket();
  if (packetSize) {
    num += 1;
    Serial.print("Received packet! Size: ");
    Serial.println(packetSize);
    int len = UDP.read(packet, 361);
    if (len > 0){
      Serial.println(packet);
      packet[len] = '\0';
//      intoArr(packet);
    }
    Serial.print("Packet number: ");
    Serial.println(num);
//    Serial.print("Packet received: ");
//    Serial.println(packet);
//    intoArr(packet);
    
  }

}
