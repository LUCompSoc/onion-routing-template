# Your Task
Complete the padding and unpadding functions
Complete the encryption and decryption functions on the relay

## Padding with PCKS#7
  padder = padding.PKCS7(128).padder() # Creating a padder of size 128 bits (16 bytes)
  padded_data = padder.update(message)  # Pad a message
  padded_data += padder.finalize() # Complete the padding

### Unpadding
  unpadder = padding.PKCS7(128).unpadder()
  unpadded_data = unpadder.update(message)
  unpadded_data += unpadder.finalize()

## Encryping with AES in ECB Mode
  cipher = Cipher(key, modes.ECB()) # The key needs to be of type AES key 
  #### This is the same as the attribute 'key' of relay
  encryptor = cipher.encryptor() 
  ciphertext = encryptor.update(ciphertext) + encryptor.finalize()

  ### Decrypting
  decrpyer = cipher.decryptor()
  ciphertext = decryptor.update(ciphertext) + decryptor.finalize()
  

## How the program works
The class Node is the parent class of Relay and Client
Messages start at the start client using the function send_message()

Each relay node automatically generates a key; you will have to manually add these to the start client (done for you in the example)

The messages are 'sent' via recurvise function calls

