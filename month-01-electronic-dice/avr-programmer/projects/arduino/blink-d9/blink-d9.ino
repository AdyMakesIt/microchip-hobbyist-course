/*
 * Month 1 Part B: blink an LED on D9
 *
 * Chip : ATmega328P-PU, 16 MHz crystal, 5 V
 * LED  : D9 (chip pin 15) -> 680 ohm -> LED -> GND
 *
 * D9 is chip pin 15 (port B, bit 1). The Arduino IDE calls it "9".
 * Used twice: on the programmer board in Build B1, and on the target board in Build B3.
 */

const int LED_PIN = 9;

void setup()
{
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    digitalWrite(LED_PIN, HIGH);   // LED on
    delay(500);                    // half a second
    digitalWrite(LED_PIN, LOW);    // LED off
    delay(500);
}
