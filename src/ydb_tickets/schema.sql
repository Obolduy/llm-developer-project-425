CREATE TABLE tickets (
    id          Utf8,       -- uuid4
    user_id     Utf8,       -- email обратившегося — идентификатор канала, не PII для маскирования
    category    Utf8,       -- bug | question | access | other
    status      Utf8,       -- open | escalated | closed
    text        Utf8,       -- текст обращения, PII уже замаскирован на границе записи
    created_at  Timestamp,
    updated_at  Timestamp,
    PRIMARY KEY (id),
    INDEX ticket_by_user GLOBAL ON (user_id)
);

CREATE TABLE messages (
    id          Utf8,       -- uuid4
    ticket_id   Utf8,       -- NULL, если реплика не привязана к тикету
    user_id     Utf8,       -- участник переписки — для сквозного учёта расхода по пользователю
    role        Utf8,       -- user | assistant
    text        Utf8,       -- текст реплики, PII уже замаскирован
    model       Utf8,       -- модель, которая отвечала (для role=assistant)
    tokens_in   Uint64,
    tokens_out  Uint64,
    latency_ms  Uint32,
    created_at  Timestamp,
    PRIMARY KEY (id),
    INDEX message_by_ticket GLOBAL ON (ticket_id)
);
