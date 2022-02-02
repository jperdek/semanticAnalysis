import sys

def split_file(inFilename, dictionary, outFilename, oldSeq, lines = 500000, header_lines = 8):
    header_part = ""
    with open(inFilename, "r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            if index > header_lines:
                break
            header_part = header_part + line
    inputFile  = open(inFilename, "rb")
    outputFile = open(dictionary + outFilename + "1.ttl", "wb")
    
    data = ""
    chunk = 1024
    file_index = 2

    oldSeqLen = len(oldSeq)
    
    file_seq_number = 0
    lines = int(lines)
    while 1:
        data = inputFile.read(chunk)
        if not data:
            break
        number_seq = data.count(oldSeq)
        file_seq_number =  file_seq_number + number_seq
        dataSize = len(data)
      
        seekLen= data.rfind(oldSeq)
        
        if file_seq_number > lines:
            file_seq_number = 0
            outputFile.write(data[:seekLen])
            outputFile.close()
            outputFile = open(dictionary + outFilename + str(file_index) + ".ttl", "wb")
            outputFile.write(header_part.encode())
            outputFile.write(data[seekLen:])
            file_index = file_index + 1
        else:
            outputFile.write(data)
          


    inputFile.close()
    outputFile.close()
 
 # \\ sequence do problem in IRI https://stackoverflow.com/questions/2833013/idn-aware-tools-to-encode-decode-human-readable-iri-to-from-valid-uri
split_file(sys.argv[1], sys.argv[2], sys.argv[3], b"\n#@", sys.argv[4])
               