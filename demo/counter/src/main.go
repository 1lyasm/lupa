package main

import (
	"net/http"
	"strconv"
)

type CounterHandler struct {
	count uint64
}

func (handler *CounterHandler) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	handler.count += 1
	w.Write([]byte(strconv.FormatUint(handler.count, 10)))
}

func main() {
    http.Handle("/", &CounterHandler{count: 0})
    http.ListenAndServe(":6789", nil)
}

