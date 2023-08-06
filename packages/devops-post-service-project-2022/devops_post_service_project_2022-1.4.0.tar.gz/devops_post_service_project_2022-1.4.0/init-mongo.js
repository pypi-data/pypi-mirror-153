db.createUser({
    user: 'root',
    pwd: 'password',
    roles: [
        {
            role: 'readWrite',
            db: 'post',
        },
    ],
});

db = new Mongo().getDB("post");

db.createCollection('users', { capped: false });
db.createCollection('post', { capped: false });