FROM base as runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

WORKDIR /app/src

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
