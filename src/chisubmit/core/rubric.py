
#  Copyright (c) 2013-2014, The University of Chicago
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  - Neither the name of The University of Chicago nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

import yaml
from chisubmit.core import ChisubmitException
import textwrap


class ChisubmitRubricException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class RubricFile(object):
    
    FIELD_COMMENTS = "Comments"
    FIELD_PENALTIES = "Penalties"
    FIELD_POINTS   = "Points"
    FIELD_TOTAL_POINTS = "Total Points"
    FIELD_POINTS_POSSIBLE = "Points Possible"
    FIELD_POINTS_OBTAINED = "Points Obtained"
    
    def __init__(self, project, points, penalties, comments):
        self.project = project
        self.points = points
        self.penalties = penalties
        self.comments = comments
        
    def __format_points(self, n):
        return str(round(n,2) if n % 1 else int(n))
        
    def to_yaml(self, include_blank_comments = False):
        # We generate the file manually to make it as human-readable as possible
        
        s = "Points:\n"
        
        total_points_possible = 0
        total_points_obtained = 0
        
        for gc in self.project.grade_components:
            s += "%s%s:\n" % (" "*4, gc.name)
            s += "%s%s: %s\n" % (" "*8, self.FIELD_POINTS_POSSIBLE, self.__format_points(gc.points))
            total_points_possible += gc.points
            if self.points[gc.name] is None:
                p = ""
            else:
                total_points_obtained += self.points[gc.name]
                p = self.__format_points(self.points[gc.name])
                
            s += "%s%s: %s\n" % (" "*8, self.FIELD_POINTS_OBTAINED, p)
            s += "\n" 
            
        penalty_points = 0.0
        if self.penalties is not None:
            s += "%s:\n" % self.FIELD_PENALTIES
            for desc, v in self.penalties.items():
                penalty_points += v
                s += "%s%s:%s\n" % (" "*4, desc, self.__format_points(v))            
            s += "\n"

        s += "%s: %s / %s\n" % (self.FIELD_TOTAL_POINTS,
                              self.__format_points(total_points_obtained + penalty_points),
                              self.__format_points(total_points_possible)) 
            
        if self.comments is not None or include_blank_comments:
            s += "\n"
            s += "%s: >\n" % self.FIELD_COMMENTS
            
            if self.comments is not None:
                for l in self.comments.strip().split("\n"):
                    for l2 in textwrap.wrap(l, initial_indent = " "*4):
                        s += l2 + "\n" 
            else:
                s += " "*4 + "None"
        
        return s
        
    def save(self, rubric_file, include_blank_comments = False):
        try:
            f = open(rubric_file, 'w')
            f.write(self.to_yaml(include_blank_comments))
            f.close()
        except IOError, ioe:
            raise ChisubmitException("Error when saving rubric to file %s: %s" % (rubric_file, ioe.meesage), ioe)
        
    @classmethod
    def from_file(cls, rubric_file, project):
        rubric = yaml.load(rubric_file)

        if not rubric.has_key(RubricFile.FIELD_POINTS):
            raise ChisubmitRubricException("Rubric file doesn't have a '%s' field." % RubricFile.FIELD_POINTS)

        if not rubric.has_key(RubricFile.FIELD_TOTAL_POINTS):
            raise ChisubmitRubricException("Rubric file doesn't have a '%s' field." % RubricFile.FIELD_TOTAL_POINTS)

        points = {}
        total_points_obtained = 0
        total_points_possible = 0
        for grade_component in project.grade_components:
            if not rubric[RubricFile.FIELD_POINTS].has_key(grade_component.name):
                raise ChisubmitRubricException("Rubric is missing '%s' points." % grade_component.name)
            
            component = rubric[RubricFile.FIELD_POINTS][grade_component.name]
            
            if not component.has_key(RubricFile.FIELD_POINTS_POSSIBLE):
                raise ChisubmitRubricException("Grade component '%s' is missing '%s' field." % (grade_component.name, RubricFile.FIELD_POINTS_POSSIBLE))

            if not component.has_key(RubricFile.FIELD_POINTS_OBTAINED):
                raise ChisubmitRubricException("Grade component '%s' is missing '%s' field." % (grade_component.name, RubricFile.FIELD_POINTS_OBTAINED))
            
            points_possible = component[RubricFile.FIELD_POINTS_POSSIBLE]
            points_obtained = component[RubricFile.FIELD_POINTS_OBTAINED]
            
            if points_possible != grade_component.points:
                raise ChisubmitRubricException("Grade component '%s' in rubric has incorrect possible points (expected %i, got %i)" %
                                                (grade_component.name, grade_component.points, points_possible))
                
            if points_obtained is not None:
                if points_obtained < 0:
                    raise ChisubmitRubricException("Grade component '%s' in rubric has negative points (%i)" %
                                                    (grade_component.name, points_obtained))
    
                if points_obtained > points_possible:
                    raise ChisubmitRubricException("Grade component '%s' in rubric has more than allowed points (%i > %i)" %
                                                    (grade_component.name, points_obtained, points_possible))

                total_points_obtained += points_obtained

            points[grade_component.name] = points_obtained
            total_points_possible += grade_component.points

        penalty_points = 0.0
        if rubric.has_key(RubricFile.FIELD_PENALTIES):
            penalties = rubric[RubricFile.FIELD_PENALTIES]
            for desc, v in penalties.items():
                if v >= 0:
                    raise ChisubmitRubricException("Rubric file has a non-negative penalty: %s (%s)" % (v, desc))
                penalty_points += v
        else:
            penalties = None
            
        if type(rubric[RubricFile.FIELD_TOTAL_POINTS]) != str:
            raise ChisubmitRubricException("Total points is not a string: %s" % rubric[RubricFile.FIELD_TOTAL_POINTS])
            
            
        total_points = rubric[RubricFile.FIELD_TOTAL_POINTS].split(" / ")
        if len(total_points) != 2:
            raise ChisubmitRubricException("Improperly formatted total points: %s" % rubric[RubricFile.FIELD_TOTAL_POINTS])
        
        if float(total_points[0]) != float(total_points_obtained) + penalty_points:
            raise ChisubmitRubricException("Incorrect number of total points obtained (Expected %.2f, got %.2f)" % 
                                           (float(total_points_obtained) + penalty_points, float(total_points[0])))
            
        if float(total_points[1]) != float(total_points_possible):
            raise ChisubmitRubricException("Incorrect number of total points obtained (Expected %.2f, got %.2f)" % 
                                           (float(total_points_possible), float(total_points[1])))
            
        if not rubric.has_key(RubricFile.FIELD_COMMENTS):
            comments = None
        else:
            comments = rubric[RubricFile.FIELD_COMMENTS]

        return cls(project, points, penalties, comments)

    @classmethod
    def from_project(cls, project, team_project = None):
        points = dict([(gc.name, None) for gc in project.grade_components])
        
        if team_project is not None:
            for gc, gc_points in team_project.grades.items():
                points[gc.name] = gc_points
        
        return cls(project, points, comments = None)
        
    
    