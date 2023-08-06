SELECT
        json_extract(simtimes, '$.counting_env.simtime_ticks') AS tick,
        GROUP_CONCAT(SUBSTR(json_extract(actuator_setpoints, '$[0].actuator_id'), -1, 1)) AS actuators,
        GROUP_CONCAT(json_extract(rewards, '$[0].reward_value')) AS reward_values,
        SUM(json_extract(rewards, '$[0].reward_value')) AS total_reward,
        SUM(SUBSTR(json_extract(actuator_setpoints, '$[0].actuator_id'), -1, 1)) * COUNT(json_extract(actuator_setpoints, '$[0].actuator_id')) AS reward_expected,
        SUM(json_extract(rewards, '$[0].reward_value'))
            = SUM(SUBSTR(json_extract(actuator_setpoints, '$[0].actuator_id'), -1, 1)) * COUNT(json_extract(actuator_setpoints, '$[0].actuator_id')) AS check_result
FROM muscle_actions
WHERE json_extract(actuator_setpoints, '$[0]._setpoint') = 1
GROUP BY tick