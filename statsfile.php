<?php

/**
 * Class StatsFile
 * @brief Statistic settings
 */
class StatsFile
{
    /** @var Output file destination */
    readonly string $file_path;
    /** @var List of chosen flags    */
    readonly array $flags;

    /**
     * @brief Constructor of the class StatsFile
     *
     * @param $flags Chosen flags to be included in output file
     * @param $path_file Output file destination
     */
    public function __construct(array $flags, string $path_file)
    {
        $this->path_file = $path_file;
        $this->flags = $flags;
    }

    /**
     * @brief Create output file
     *
     * @param #lof_stats List of all gathered stats
     */
    public function flushFile(array $lof_stats)
    {
        $file = fopen($file_path, "w");
        foreach ($flags as $key)
        {
            fwrite($file, $lof_stats[$key]);
            fwrite($file, "\n");
        }
        fclose($file);
    }
}
?>
