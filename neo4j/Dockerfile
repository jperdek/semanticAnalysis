FROM neo4j:4.4.3

ENV NEO4J_AUTH=neo4j/neo4j1

COPY ./conf/co-occurrence/neo4j.conf /conf/neo4j.conf
RUN --mount=target=/dumps,type=bind,source=dumps neo4j-admin load --from=/dumps/probase-dump.dump --database=neo4j --force
CMD [ "neo4j" ]