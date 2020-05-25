CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `v_materials` AS
    SELECT 
        `m`.`id` AS `id`,
        (CASE
            WHEN (`m`.`brand` IS NULL) THEN '-'
            ELSE `m`.`brand`
        END) AS `brand`,
        (CASE
            WHEN (`m`.`platform` IS NULL) THEN '-'
            ELSE `m`.`platform`
        END) AS `platform`,
        (CASE
            WHEN (`m`.`code` IS NULL) THEN '-'
            ELSE `m`.`code`
        END) AS `code`,
        `m`.`type` AS `type`,
        (CASE
            WHEN (`m`.`name` IS NULL) THEN '-'
            ELSE `m`.`name`
        END) AS `name`,
        (SELECT 
                `u`.`owner_name`
            FROM
                `d_users` `u`
            WHERE
                (`u`.`user_id` = `m`.`creater`)) AS `usr`,
        (CASE
            WHEN (`m`.`tdp` IS NULL) THEN '-'
            ELSE `m`.`tdp`
        END) AS `tdp`,
        DATE_FORMAT(`m`.`create_date`, '%Y-%m-%d') AS `createdate`,
        (CASE
            WHEN (`m`.`spec` IS NULL) THEN '-'
            ELSE `m`.`spec`
        END) AS `spec`
    FROM
        (`d_materials` `m`
        JOIN `d_users` `S`)
    WHERE
        ((`m`.`creater` = `S`.`user_id`)
            AND (`m`.`iswork` = '1'))
    ORDER BY `m`.`id` DESC ;
    
    CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `v_recyclebin` AS
    SELECT 
        `m`.`id` AS `id`,
        (CASE
            WHEN (`m`.`brand` IS NULL) THEN '-'
            ELSE `m`.`brand`
        END) AS `brand`,
        (CASE
            WHEN (`m`.`platform` IS NULL) THEN '-'
            ELSE `m`.`platform`
        END) AS `plat`,
        (CASE
            WHEN (`m`.`code` IS NULL) THEN '-'
            ELSE `m`.`code`
        END) AS `co`,
        `m`.`type` AS `type`,
        (CASE
            WHEN (`m`.`name` IS NULL) THEN '-'
            ELSE `m`.`name`
        END) AS `name`,
        (SELECT 
                `u`.`owner_name`
            FROM
                `d_users` `u`
            WHERE
                (`u`.`user_id` = `m`.`creater`)) AS `usr`,
        (CASE
            WHEN (`m`.`tdp` IS NULL) THEN '-'
            ELSE `m`.`tdp`
        END) AS `tdp`,
        DATE_FORMAT(`m`.`create_date`, '%Y-%m-%d') AS `createdate`,
        (CASE
            WHEN (`m`.`spec` IS NULL) THEN '-'
            ELSE `m`.`spec`
        END) AS `spec`
    FROM
        (`d_materials` `m`
        JOIN `d_users` `S`)
    WHERE
        ((`m`.`creater` = `S`.`user_id`)
            AND (`m`.`iswork` = '0'))
    ORDER BY `m`.`id` DESC
