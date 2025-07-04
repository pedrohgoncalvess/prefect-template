FROM prefecthq/prefect:3.2.6-python3.12

WORKDIR /root/flows

COPY . .

RUN pip install --no-cache-dir -r requirements.prefect.txt

CMD ["bash"]