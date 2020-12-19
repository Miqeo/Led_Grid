
#include<ESP8266WiFi.h>
#include<WiFiUdp.h>
#include<Adafruit_NeoPixel.h>

#define LED_PIN D4
#define LED_COUNT 30

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

#define ssid "primavera-2.4G"//"akquinet_goscie"//
#define pass "trudnehaslo"//"Goscie_qwertyuiop"//
#define udpPort 4210

WiFiUDP UDP;
char packet[361];

int num = 0;

void setup() {
  
   
  Serial.begin(115200);
  Serial.println();

  WiFi.begin(ssid, pass);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.print(ssid);

  while (WiFi.status() != WL_CONNECTED){
    delay(100);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  UDP.begin(udpPort);
  Serial.print("Listening on UDP port ");
  Serial.println(udpPort);

  strip.begin();
  strip.setBrightness(30);
  strip.show();
}

long hstol(String recv){
  char c[recv.length() + 1];
  recv.toCharArray(c, recv.length() + 1);
  return strtol(c, NULL, 16); 
}

char *multi_tok(char *input, char *delimiter) {
    static char *string;
    if (input != NULL)
        string = input;

    if (string == NULL)
        return string;

    char *end = strstr(string, delimiter);
    if (end == NULL) {
        char *temp = string;
        string = NULL;
        return temp;
    }

    char *temp = string;

    *end = '\0';
    string = end + strlen(delimiter);
    return temp;
}

void showPixels(long pixels[30][3]){
  
  int width = 6;
  int height = 5;

  int stepper = (width % 2 == 0) ? width -1 : width;
  int perWidth = stepper;

  int current = 1;

  for(int i = 0; i < width * height; i++){
    
    int current = int(ceil(i / width)) % 2;
    
    if(current % 2 == 0){
      strip.setPixelColor(i, pixels[i][0], pixels[i][1], pixels[i][2]);
      
      perWidth = stepper;
      
    }
    else{
      strip.setPixelColor(i + perWidth, pixels[i][0], pixels[i][1], pixels[i][2]);
      
      perWidth -= 2;
    }
//    Serial.print(pixels[i][0]);
//    Serial.print(" ");
//    Serial.print(pixels[i][1]);
//    Serial.print(" ");
//    Serial.print(pixels[i][2]);
//    Serial.println();
      
    
    
  }
  
  strip.show();
  
}

void intoArr(char bytes[360]){

  int size = 360;
  int count = 90;
  
  long pixels[360];
  int offset = 1;
  memmove(bytes+offset, bytes+offset+1, strlen(bytes)-offset);
  
  char *p = multi_tok(bytes, "0x");
  
  for(int i = 0; i < size; i++){
    pixels[i] = hstol(p);
    p = multi_tok(NULL, "0x");
  }

  
  int j = 0;
  long pixelsSorted[30][3] = {};
  
  for (int a = 0; a < 30; ++a) {
    for (int b = 0; b < 3; ++b) {
      pixelsSorted[a][b] = pixels[j];
      j += 1;
    }
  }
  
  
  
  showPixels(pixelsSorted);
}

void loop() {
  
  
  int packetSize = UDP.parsePacket();
  if (packetSize) {
    num += 1;
    Serial.print("Received packet! Size: ");
    Serial.println(packetSize);
    int len = UDP.read(packet, 361);
    if (len > 0){
      Serial.println(packet);
      packet[len] = '\0';
      intoArr(packet);
    }
    Serial.print("Packet number: ");
    Serial.println(num);
//    Serial.print("Packet received: ");
//    Serial.println(packet);
//    intoArr(packet);
    
  }
  
}
