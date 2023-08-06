package nervos

import (
	"encoding/hex"
	"fmt"
	"strings"

	"github.com/MixinNetwork/mixin/crypto"

	"github.com/btcsuite/btcutil/bech32"
)

var (
	NervosChainBase string
	NervosChainId   crypto.Hash
)

func init() {
	NervosChainBase = "d243386e-6d84-42e6-be03-175be17bf275"
	NervosChainId = crypto.NewHash([]byte(NervosChainBase))
}

func VerifyAssetKey(assetKey string) error {
	if assetKey == NervosChainBase {
		return nil
	}
	return fmt.Errorf("invalid nervos asset key %s", assetKey)
}

func VerifyAddress(address string) error {
	if strings.TrimSpace(address) != address {
		return fmt.Errorf("invalid nervos address %s", address)
	}
	prefix, payload, err := DecodeAddress(address)
	if err != nil {
		return fmt.Errorf("invalid nervos address %s %s", address, err)
	}
	if prefix != PrefixMainNet {
		return fmt.Errorf("invalid nervos address %s", address)
	}
	if len(payload) <= 1 {
		return fmt.Errorf("invalid nervos address %s", address)
	}
	if payload[0] != ShortFormat {
		return fmt.Errorf("invalid nervos address %s", address)
	}

	if payload[1] != CodeHashSingleIndex {
		return fmt.Errorf("invalid nervos address %s", address)
	}
	ckbAddress, err := EncodeAddress(payload)
	if err != nil {
		return fmt.Errorf("invalid nervos address %s %s", address, err)
	}
	if address != ckbAddress {
		return fmt.Errorf("invalid nervos address %s", address)
	}
	return nil
}

func VerifyTransactionHash(hash string) error {
	if len(hash) != 66 {
		return fmt.Errorf("invalid nervos transaction hash %s", hash)
	}
	if !strings.HasPrefix(hash, "0x") {
		return fmt.Errorf("invalid nervos transaction hash %s", hash)
	}
	if strings.ToLower(hash) != hash {
		return fmt.Errorf("invalid nervos transaction hash %s", hash)
	}
	h, err := hex.DecodeString(hash[2:])
	if err != nil {
		return fmt.Errorf("invalid nervos transaction hash %s %s", hash, err.Error())
	}
	if len(h) != 32 {
		return fmt.Errorf("invalid nervos transaction hash %s", hash)
	}
	return nil
}

func GenerateAssetId(assetKey string) crypto.Hash {
	switch assetKey {
	case NervosChainBase:
		return NervosChainId
	default:
		panic(assetKey)
	}
}

const (
	ShortFormat         byte = 1
	CodeHashSingleIndex byte = 0
	PrefixMainNet            = "ckb"
)

func EncodeAddress(payload []byte) (string, error) {
	data, err := bech32.ConvertBits(payload, 8, 5, true)
	if err != nil {
		return "", err
	}
	address, err := bech32.Encode(PrefixMainNet, data)
	if err != nil {
		return "", err
	}
	return address, nil
}

func DecodeAddress(address string) (prefix string, payload []byte, err error) {
	prefix, data, err := bech32.Decode(address)
	if err != nil {
		return "", nil, err
	}
	if prefix != PrefixMainNet {
		return "", nil, err
	}
	payload, err = bech32.ConvertBits(data, 5, 8, false)
	if err != nil {
		return "", nil, err
	}
	return prefix, payload, nil
}
