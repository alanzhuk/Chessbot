//setting up pins
int xDrive = 
int xDir = 
int yDrive = 
int yDir = 
int magnet = 
int button = 
//variables for the split function
string strCache = "";
int arrayCache [3];
int spaces = 0;
int local = 0;
//key variables
int directions [3];
int count = 0;
int xPos = 0;
int xPos = 0;
int inter; //this is used to find the intermediary between the Ys to avoid colissions(I know misspelled)
int coordinates [65] [2]{
  {,}//1
  {,}//2
  {,}//3
  //...until the discard at 65
}
rate = 50; //changes how many pulses occur every millisecond. 
void setup() {
  Serial.begin(9600);
  using namespace std;
  //setting up pins
  pinMode(xDrive,OUTPUT);
  pinMode(xDir,OUTPUT);
  pinMode(yDrive,OUTPUT);
  pinMode(yDir,OUTPUT);
  pinMode(magnet,OUTPUT);
  pinMode(button, INPUT);
}
int split(string code){
  spaces = 0;
  strCache = "";
  for (int i = 0; i < code.size();i++){
     if (code[i] == " "){
      stringstream local(strCache);
      arrayCache[spaces] = local;
      spaces ++; 
      strCache = "";
     }
     else{
      strCache = strCache + code[i];
     }
  }
  if(count < 2){
    arrayCache[2] = 0;
  }
  return(arraycache);
}
void motors(int pos, bool isX){ //first is the position you want it to go to, second if it's affecting the X axis
  if(isX){
    while (xPos != pos):
      if xPos > pos{
        xpos--; 
        digitalWrite(xDir, HIGH); //CHANGE - NO IDEA WHICH WAY THE DIRECTION MAKES IT GO
        digitalWrite(xDrive, HIGH);
        delay(rate);
      }
      else{
        xpos++;
        digitalWrite(xDir, LOW); //CHANGE - NO IDEA WHICH WAY THE DIRECTION MAKES IT GO
        digitalWrite(xDrive, HIGH);
        delay(rate);
      }
      digitalWrite(xDrive, LOW);
  }
  else:
    while (yPos != pos):
      if yPos > pos{
        ypos--; 
        digitalWrite(yDir, HIGH); //CHANGE - NO IDEA WHICH WAY THE DIRECTION MAKES IT GO
        digitalWrite(yDrive, HIGH);
        delay(rate);
      }
      else{
        ypos++;
        digitalWrite(yDir, LOW); //CHANGE - NO IDEA WHICH WAY THE DIRECTION MAKES IT GO
        digitalWrite(yDrive, HIGH);
        delay(rate);
      }
      digitalWrite(yDrive, LOW);
}
void loop() {
  motors(0,true);
  motors(0,false);
  digitalWrite(magnet,LOW);
  if(digitalRead(button)){
    Serial.println("pressed");
    if (Serial.available() > 0) {
      directions = split(Serial.readStringUntil('\n'));
      //checks if a piece has been taken
      if directions[2] != 0{
        //goes to the taken piece
        motors(coordinates[directions[1]][0],true);
        motors(coordinates[directions[1]][1],false);
        if (yPos > coordinates[65][1]){
          inter = yPos - coordinates[directions[1]-8][1];
          inter = inter/2;
          inter = inter + coordinates[directions[1]-8][1];
        }
        else{
          inter = coordinates[directions[1]+8][1] - yPos;
          inter = inter/2;
          inter = inter + yPos;
        }
        motors(inter,false);
        if (xPos > coordinates[65][0]){
          inter = xPos - coordinates[directions[1]-1][0];//CHANGE potentially, because the -1 might have to be a +1 depending on how the grid coresponds with motor movement. 
          inter = inter/2;
          inter = inter + coordinates[directions[1]-1][0];
        }
        else{
          inter = coordinates[directions[1]+1][0] - xPos;
          inter = inter/2;
          inter = inter + xPos;
        }
        motors(inter,true);
        motors(coordinates[65][1], false);
        motors(coordinates[65][0], true);
      }
      motors(coordinates[directions[0]][0],true);
      motors(coordinates[directions[0]][1],false);
      if (yPos > coordinates[directions[1]][1]){
        inter = yPos - coordinates[directions[0]-8][1];
        inter = inter/2;
        inter = inter + coordinates[directions[0]-8][1];
      }
      else{
        inter = coordinates[directions[0]+8][1] - yPos;
        inter = inter/2;
        inter = inter + yPos;
      }
      motors(inter,false);
      motors(coordinates[directions[1]][0],true)
      motors(coordinates[directions[1]][1],false)
    }
  }
}
