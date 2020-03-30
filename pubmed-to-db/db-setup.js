const knex = require('knex')({
  client: 'mysql',
  connection: {
    host: '127.0.0.1',
    user: 'root',
    password: 'password',
    database: 'pubmed'
  },
  migrations: {
    tableName: 'migrations'
  }
});

async function setup() {
  await knex.schema.createTable('articles', table => {
    table.charset('utf8mb4');

    table.bigInteger('pmid').primary();
    table.text('title');
    table.text('abstract');
    table.string('journal');
    table.string('journal_abbr');
    table.string('journal_issn');
    table.integer('publication_year');
  });

  console.log('Sucessfully created articles table');
  console.log('Exiting...');

  process.exit(0);
}

setup();
