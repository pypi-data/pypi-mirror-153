package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/ed25519"
	"crypto/rand"
	"encoding/base64"
	"encoding/binary"
	"io"
	"time"

	"golang.org/x/crypto/curve25519"

	"crypto/sha512"
)

/*
#include <stdint.h>
*/
import "C"

func PrivateKeyToCurve25519(curve25519Private *[32]byte, privateKey ed25519.PrivateKey) {
	h := sha512.New()
	h.Write(privateKey.Seed())
	digest := h.Sum(nil)

	digest[0] &= 248
	digest[31] &= 127
	digest[31] |= 64

	copy(curve25519Private[:], digest)
}

func encryptEd25519PIN(pin, pinTokenBase64, sessionId, privateKey string, iterator uint64) (string, error) {
	privateBytes, err := base64.RawURLEncoding.DecodeString(privateKey)
	if err != nil {
		return "", err
	}

	private := ed25519.PrivateKey(privateBytes)
	public, err := base64.RawURLEncoding.DecodeString(pinTokenBase64)
	if err != nil {
		return "", err
	}
	var keyBytes, curvePriv, pub [32]byte
	PrivateKeyToCurve25519(&curvePriv, private)
	copy(pub[:], public[:])
	curve25519.ScalarMult(&keyBytes, &curvePriv, &pub)

	pinByte := []byte(pin)
	timeBytes := make([]byte, 8)
	binary.LittleEndian.PutUint64(timeBytes, uint64(time.Now().Unix()))
	pinByte = append(pinByte, timeBytes...)
	iteratorBytes := make([]byte, 8)
	binary.LittleEndian.PutUint64(iteratorBytes, iterator)
	pinByte = append(pinByte, iteratorBytes...)
	padding := aes.BlockSize - len(pinByte)%aes.BlockSize
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	pinByte = append(pinByte, padtext...)
	block, err := aes.NewCipher(keyBytes[:])
	if err != nil {
		return "", err
	}
	ciphertext := make([]byte, aes.BlockSize+len(pinByte))
	iv := ciphertext[:aes.BlockSize]
	_, err = io.ReadFull(rand.Reader, iv)
	if err != nil {
		return "", err
	}
	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext[aes.BlockSize:], pinByte)
	return base64.RawURLEncoding.EncodeToString(ciphertext), nil
}

//export EncryptEd25519PIN
func EncryptEd25519PIN(pin, pinTokenBase64, sessionId, privateKey *C.char, interator C.uint64_t) *C.char {
	_pin := C.GoString(pin)
	_pinTokenBase64 := C.GoString(pinTokenBase64)
	_sessionId := C.GoString(sessionId)
	_privateKey := C.GoString(privateKey)
	_iterator := uint64(interator)
	_result, _err := encryptEd25519PIN(_pin, _pinTokenBase64, _sessionId, _privateKey, _iterator)
	if _err != nil {
		return renderError(_err)
	}
	return renderData(_result)
}
