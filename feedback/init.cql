drop keyspace if exists feedback_data;
create keyspace feedback_data with replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '2'};


use feedback_data;
create table feedbacks ( id UUID PRIMARY KEY, feedback_text text );


insert into feedback_data.feedbacks ( id, feedback_text )
VALUES( uuid(), 'Pretty Good' );

insert into feedback_data.feedbacks ( id, feedback_text )
VALUES( uuid(), 'Ohh, very nice' );

insert into feedback_data.feedbacks ( id, feedback_text )
VALUES( uuid(), 'I like it!' );
