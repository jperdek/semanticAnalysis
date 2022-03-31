FROM neo4j:4.4.3 AS build-stage
LABEL stage=builder
ENV NEO4J_AUTH=neo4j/perdekj
RUN --mount=target=/dumps,type=bind,source=dumps neo4j-admin load --from=/dumps/neo4j-yago-dump.dump --database=neo4j --force


FROM neo4j:4.4.3 AS final-image
ENV NEO4J_AUTH=neo4j/perdekj
COPY --from=build-stage /data/databases /data/databases
COPY --from=build-stage /data/transactions /data/transactions
COPY ./conf/neo4j.conf /conf/neo4j.conf
CMD [ "neo4j" ]