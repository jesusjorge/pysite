import base64
import hashlib

challenge = input("Enter the text string: ")
stop = int(input("Enter the stop length: "))
sequence = int(input("Enter the sequence: "))

iLength = 1
while iLength <= stop:
    if sequence % 7654321 == 0:
        print(sequence)
    check = base64.b64encode(hashlib.sha512((challenge + str(sequence)).encode('utf-8')).digest()).decode('utf-8')
    if challenge[0:iLength] in check:
        print(f"\n{sequence}: {check}\n")
        iLength = iLength + 1
    else:
        sequence = sequence + 1
    
print("Finish")
