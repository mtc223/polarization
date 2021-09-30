int inputs[6];
int outputs[14];
int stepdir[] = {3,2,5,4};

void setup() {
  Serial.begin(9600);
  for(int i = 0; i < 4; i++){
    pinMode(stepdir[i],OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    String incomingstring = Serial.readString();
    //incomingstring.remove(incomingstring.length()-1);
    parseInput(incomingstring);
  }
}

int parseInput(String in){
  int del0 = in.indexOf(":");
  int del1 = in.indexOf(":",del0+1);
  String arg0="";
  String arg1="";
  String arg2="";
  if(del0==del1){
    arg0=in;
  }
  else if(del0>del1){
    arg0=in.substring(0,del0);
    arg1=in.substring(del0+1);
  }
  else{
    arg0=in.substring(0,del0);
    arg1=in.substring(del0+1,del1);
    arg2=in.substring(del1+1);
  }
  return encode(arg0,arg1,arg2);
}

int encode(String arg0, String arg1, String arg2){
  if(arg0=="echo"){
    Serial.println("echo");
  }
  else if(arg0=="turn"){
    turn(arg1.toInt(), arg2.toInt());
  }
  else if(arg0=="read"){
    read(arg1.toInt());
  }
  else if(arg0=="readad"){
    readAD(arg1.toInt());
  }
  else if(arg0=="reset"){
    for(int i=0; i<14; i++){
      encode("in",String(i),"off");
      encode("out",String(i),"off");
    }
    Serial.println("Pins are reset.");
  }
  else if(arg0=="print"){
    printIO();
  }
  else if(arg0=="in"){
    if(arg1.toInt()<0 || arg1.toInt()>5){
       Serial.print("Something went wrong");
    }
    else if(arg1==""){
      int incount = 0;
      for(int i=0; i<6; i++){
        if(inputs[i]!=0){
          incount++;
        }
      }
      Serial.println(incount);
    }
    else{
      if(arg2=="off"){
        inputs[arg1.toInt()]=0;
      }
      else{
        inputs[arg1.toInt()]=1;
      }
    }
  }
  else if(arg0=="out"){
    if(arg1.toInt()<0 || arg1.toInt()>13){
       return -1;
    }
    else{
      if(arg2=="off"||arg2=="Off"){
        outputs[arg1.toInt()]=0;
        analogWrite(arg1.toInt(),0);
      }
      else{
        pinMode(arg1.toInt(),OUTPUT);
        if(arg2.toInt()!=0){
          analogWrite(arg1.toInt(),arg2.toInt());
          outputs[arg1.toInt()]=arg2.toInt();
        }
        else{
          analogWrite(arg1.toInt(),255);
          outputs[arg1.toInt()]=255;
        }
      }
    }
  }
  else{
    Serial.println("Something went wrong");
  }
  return 1;
}

void printIO(){
  Serial.print("Inputs:");
  for(int i=0; i<6; i++){
    Serial.print(String(inputs[i])+",");
  }
  Serial.println();
  Serial.print("Outputs:");
  for(int i=0; i<14; i++){
    Serial.print(String(outputs[i])+",");
  }
  Serial.println();
}

void read(int duration){
    int incount=0;
    int inmap[6]={0,0,0,0,0,0};
    Serial.print("Reading: {i,");
    for(int i=0; i<6; i++){
      if(inputs[i]!=0){
        inmap[incount]=i;
        incount++;
        Serial.print("A"+String(i) + ",");
      }
    }
    Serial.print("}");
    int arr[incount][duration];
    unsigned long tim = millis();
    for(int i=0; i<duration; i++){
      for(int j=0; j<incount; j++){
        int pin = 14+inmap[j];
        arr[j][i] = analogRead(pin);
      }
    }
    Serial.println("Time: " + String(millis()-tim));
    for(int i=0; i<duration; i++){
      Serial.print(String(i)+",");
      for(int j=0; j<incount; j++){
        Serial.print(String(arr[j][i])+",");
      }
      Serial.println();
    }
}
void readAD(int duration){

  int arr[duration];
  unsigned long tim;
  int counter = 0;
  while(counter < duration){
    tim = millis();
    while(millis()-tim < 5){
      Serial.println(digitalRead(A0));
    }
    //counter++;
  }
  for(int i = 0; i<duration; i++){
    //Serial.println(String(arr[i]));
  }
}

void turn(int motor, int angle){
  digitalWrite(stepdir[motor*2+1],HIGH);
  if(angle > 0){
    digitalWrite(stepdir[motor*2+1],LOW);
  }
  angle = abs(angle);
  //3200 steps=35 degrees
  int rem = angle%35;
  int steps = (((angle-rem)/35)*3200)+map(rem,0,35,0,3200);
  for(int x = 0; x < steps; x++) {
    digitalWrite(stepdir[motor*2],HIGH);
    delayMicroseconds(500);
    digitalWrite(stepdir[motor*2],LOW);
    delayMicroseconds(500);
  }
}
