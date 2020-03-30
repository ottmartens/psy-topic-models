const xml2json = require('xml2json');
const readline = require('readline');
const fs = require('fs');

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

const xmlFile = process.argv[2];

const lineReader = readline.createInterface({
  input: fs.createReadStream(xmlFile)
});

const articleStartRegex = /<PubmedArticle>/;
const articleEndRegex = /<\/PubmedArticle>/;

let isInArticle = false;
let articleCount = 0;
let currentArticle = [];
let skippedArticleIndices = [];

let lastArticle;

lineReader.on('line', async line => {
  if (line.match(articleStartRegex)) {
    isInArticle = true;
  }

  if (isInArticle) {
    currentArticle.push(line);
  }

  if (line.match(articleEndRegex)) {
    lastArticle = currentArticle.join('\n');
    currentArticle = [];
    isInArticle = false;

    try {
      await handleXMLArticle(lastArticle);
    } catch (err) {
      console.error(err);
      lineReader.close();
      process.exit(1);
    }
  }
});

lineReader.on('close', () => {
  console.log('Stream closed, exiting...');
  console.log(`Processed ${articleCount} articles`);
  console.log('Skipped articles:');
  console.log(skippedArticleIndices.join('\n'));

  setTimeout(() => process.exit(0), 2000);
});

const handleXMLArticle = async xml => {
  const json = xml2json.toJson(xml);
  const articleObject = JSON.parse(json).PubmedArticle.MedlineCitation;

  const article = getArticleFields(articleObject);

  if (!article.abstract) return;

  articleCount++;

  if (articleCount % 10000 === 0) {
    console.log(`Processed ${articleCount} articles`);
  }

  try {
    await knex('articles').insert(article);
  } catch (err) {
    skippedArticleIndices.push(articleCount);
  }
};

const getArticleFields = article => {
  const journal_year = Number(
    parseValue(article, 'Article', 'Journal', 'JournalIssue', 'PubDate', 'Year')
  );
  const article_year = Number(
    parseValue(article, 'Article', 'ArticleDate', 'Year')
  );

  return {
    pmid: Number(parseValue(article, 'PMID', '$t')),
    title: parseValue(article, 'Article', 'ArticleTitle'),
    abstract: parseValue(article, 'Article', 'Abstract', 'AbstractText'),
    journal: parseValue(article, 'Article', 'Journal', 'Title'),
    journal_abbr: parseValue(article, 'Article', 'Journal', 'ISOAbbreviation'),
    journal_issn: parseValue(article, 'Article', 'Journal', 'ISSN'),
    publication_year: article_year || journal_year || null
  };
};

function parseValue(obj, ...args) {
  const value = getNestedPropterty(obj, ...args);

  return handleMultipleValues(value);
}

function getNestedPropterty(obj, ...args) {
  return args.reduce((obj, level) => obj && obj[level], obj);
}

function handleMultipleValues(value) {
  switch (typeof value) {
    case 'string':
      return value;
    case 'object':
      if (value.length) {
        return value.map(subfield => subfield['$t']).join(' ');
      } else {
        return value['$t'] || null;
      }
    default:
      return null;
  }
}
