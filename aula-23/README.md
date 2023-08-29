## Configurando banco de dados no AWS RDS

Assim como o S3, o RDS (Relational Database Service) é um serviço da AWS. Nele você pode criar bancos de dados relacionais, como Posrgres e MySQL, entre outros.

Ele possui um free tier, com 12 meses gratuitos para novas contas que inclui 750h por mês de uso de instâncias db.t2.micro, db.t3.micro e db.t4g.micro, 20GB de armazenamento de banco de dados de uso geral e 20GB de armazenamento para backups. Apóis ultrapassar os 12 meses ou os limites descritos acima, o pagamento é por utilização.

Algumas vantagens:
- Disponibilidade;
- Backups automatizados do banco e dos logs de transação - no free tier esses dados são mantidos por 7 dias, mas é configurável até 35 dias;
- Escalabilidade - conforme a necessidade de armazenamento cresce, você pode aumentar a capacidade da isntância, isso sem o banco ficar inativo.
- Segurança - permite criptografia dos dados, permite selecionar endereços de IP que podem acessar o banco, entre outros.