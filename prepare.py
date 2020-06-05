import api

def main():
    """Подготовительный скрипт для запуска на контакте теста всех методов.
    Сначала подготавливаем данные - получаем список файлов размером более 2Мб.
    Потом получаем список своих uns записей, получаем uns записей которыен уже в статес отправки.
    Их преобразуем в список ников.
    Далее идёт процесс:
    * сначала отправки двух писем с аттачами,
    * потом отправка 2ух uns если их нет в спискее исходящих
    * и отправка двух инвойсов на карту контакту"""

    # Settings
    token = "5E1A9443A7DA0B4C3D300D5F59AF793C"
    apiPort = "20008"
    contactPk = "79622FD2FD85B96BBD85A505EE3368680A3A40E528B9B5C5F214300FE6440E4D"
    contactCard = "D579006B546BDD56"
    
    ## Action
    # Prepare data for script
    u = api.Utopia("http://127.0.0.1:"+apiPort+"/api/1.0",token)    

    _, local_files = u.getFilesFromManager()
    gt_2Mb_files = [file for file in local_files if file['totalSize'] > 2000000]

    _, my_uns_records = u.unsRegisteredNames()
    _, outgoing_uns_transfers = u.outgoingUnsTransfer()
    outgoing_uns_names = [uns['nick'] for uns in outgoing_uns_transfers]

    # Send 2 emails with attachments
    print(u.sendEmailMessage([contactPk], "Python API 1", "API method sendEmailMessage testing \n with attach", gt_2Mb_files[0]['id']))
    print(u.sendEmailMessage([contactPk], "Python API 2", "API method sendEmailMessage testing \n with attach", gt_2Mb_files[-1]['id']))

    # Transfer 2 uns records
    i = 0
    while i < 2:
        uns = [uns['nick'] for uns in my_uns_records if str(uns['nick']).upper() not in outgoing_uns_names]
        print(u.requestUnsTransfer(uns[i], contactPk))
        i += 1

    # Send 2 Invoices
    print(u.sendInvoice('Invoice #1', contactCard, 1.1))
    print(u.sendInvoice('Invoice #2', contactCard, 1.2))
    
    del u


if __name__ == "__main__":
    main()
