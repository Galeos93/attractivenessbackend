FROM yoanlin/opencv-python3:latest

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV CONFIG /app/resources/config.yaml

# Install production dependencies.
RUN pip install --no-cache-dir -r dependencies/requirements.txt \
&& pip install --no-cache-dir torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
&& pip install --no-cache-dir dependencies/facetoolbox-1.0.0-py3-none-any.whl \
&& rm -rf dependencies/facetoolbox-1.0.0-py3-none-any.whl \
&& pip install --no-cache-dir gunicorn

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --max-requests 20 wsgi:app
