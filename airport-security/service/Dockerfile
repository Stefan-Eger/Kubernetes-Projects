# start from slim python images
FROM python:slim

# working directory inside image
WORKDIR /usr/src/app

# copy python library requirements.txt
COPY requirements.txt ./

# install those requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY . .

# execute application
CMD ["python", "-u" ,"./collector.py"]