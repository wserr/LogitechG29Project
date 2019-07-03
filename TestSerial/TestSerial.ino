
void setup()
{
    Serial.begin(9600);
}

void loop()
{
    if (Serial.available() > 1)
    {
        char buf[4];
        Serial.readBytes(buf,4);
        Serial.println(buf);
    }

}