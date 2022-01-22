import sys

def replace_sequence(inFilename, outFilename, oldSeq, newSeq):
    inputFile  = open(inFilename, "rb")
    outputFile = open(outFilename, "wb")

    data = ""
    chunk = 1024

    oldSeqLen = len(oldSeq)

    while 1:
        data = inputFile.read(chunk)

        dataSize = len(data)
        seekLen= dataSize - data.rfind(oldSeq) - oldSeqLen
        if seekLen > oldSeqLen:
            seekLen = oldSeqLen

        data = data.replace(oldSeq, newSeq)
        outputFile.write(data)
        inputFile.seek(-seekLen, 1) 
        outputFile.seek(-seekLen, 1)

        if dataSize < chunk:
            break

    inputFile.close()
    outputFile.close()
 
 # \\ sequence do problem in IRI https://stackoverflow.com/questions/2833013/idn-aware-tools-to-encode-decode-human-readable-iri-to-from-valid-uri
replace_sequence(sys.argv[1], sys.argv[2], b"\\u0022", b"_quote_")
               