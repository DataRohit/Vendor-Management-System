# Use the official PostgreSQL 16 Alpine image as the base image
FROM docker.io/postgres:16-alpine


# Copy the maintenance scripts from the directory to /usr/bin/maintenance inside the container
COPY ./compose/postgres/maintenance /usr/bin/maintenance


# Change permissions to make the maintenance scripts executable
RUN chmod +x /usr/bin/maintenance/*


# Move the maintenance scripts from /usr/bin/maintenance to /usr/bin
# and remove the empty maintenance directory
RUN mv /usr/bin/maintenance/* /usr/bin \
    && rmdir /usr/bin/maintenance
