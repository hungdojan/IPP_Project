<?php
/**
 * @brief Class StatsFile and Stats for outputing statistics about source code
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @file    stats.php
 * @author  Hung Do
 * @date    16.02.2022
 */

require_once 'error.php';

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


/**
 * Class Stats
 * @brief Static class with all available stats value of the source code
 */
class Stats
{
    /** @var Table with all stats */
    public array $lof_stats = array( 
        "--loc"       => 0,
        "--comments"  => 0,
        "--labels"    => 0,
        "--jumps"     => 0,
        "--fwjumps"   => 0,
        "--backjumps" => 0,
        "--badjumps"  => 0
    );
    /** @var List of StatsFile instances */
    private array $lof_files;
    private array $used_file_names;

    /**
     * @breif Constructor of the class Stats
     */
    public function __construct()
    {
        // TODO:
    }

    /**
     * @brief Push new instance of StatsFile to $lof_files
     *
     * Check if file_path (output file destination) is unique.
     * If not the function returns given error code.
     *
     * @param $flags List of chosen flags
     * @param file_name Output fil destination
     * @return 0 or error code
     */
    public function appendStatsInstance(array $flags, string $file_path)
    {
        // checks whether file_path is already in use
        if (in_array($file_path, $used_file_names))
            return 99; // TODO: error code

        array_push($lof_files, new StatsFile($flags, $file_path));
        array_push($used_file_names, $file_path);
        return Error::NO_ERROR;
    }

    /**
     * @brief Creates all statistics file
     *
     * @return 0 or error code
     */
    public function flushFiles()
    {
        // Go through all instances of StatsFile
        // and creates a file for each of them
        foreach ($lof_sf as $item)
            $item->flushFile($lof_stats);
    }
}
?>
